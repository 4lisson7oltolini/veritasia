"""Veritas AI - núcleo do agente de pesquisa.

Fluxo: pergunta -> Gemini planeja buscas -> Tavily pesquisa -> Gemini sintetiza com citações.
"""
import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types
from tavily import TavilyClient

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")  # ajuste se quiser outro modelo
gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

PLANNER_PROMPT = """Você planeja pesquisas na web. Dada a pergunta do usuário, gere de 2 a 4
consultas de busca curtas e diferentes entre si (incluindo ao menos uma que procure
evidências CONTRÁRIAS à hipótese implícita na pergunta). Responda só com JSON:
{"queries": ["...", "..."]}"""

ANALYST_PROMPT = """Você é a Veritas AI, analista de pesquisa imparcial.
Use APENAS as fontes numeradas fornecidas. Regras:
- Cite cada afirmação relevante com [n].
- Se as fontes divergirem, mostre as duas posições.
- Se as fontes não bastarem, diga claramente o que não foi possível confirmar.
- Termine com 'Nível de confiança: alto/médio/baixo' e uma frase justificando.
Responda em português, de forma objetiva."""


def gerar(contents: str, config: types.GenerateContentConfig, tentativas: int = 5):
    """Chama o Gemini com novas tentativas em erros temporários (429/500/503/504)."""
    for i in range(tentativas):
        try:
            return gemini.models.generate_content(model=MODEL, contents=contents, config=config)
        except errors.APIError as e:
            if e.code not in (429, 500, 503, 504) or i == tentativas - 1:
                raise
            espera = 2 ** (i + 1)  # 2, 4, 8, 16 s
            print(f"   (Gemini ocupado, erro {e.code}; nova tentativa em {espera}s...)")
            time.sleep(espera)


def plan_queries(question: str) -> list[str]:
    resp = gerar(
        question,
        types.GenerateContentConfig(
            system_instruction=PLANNER_PROMPT,
            temperature=0.2,
            response_mime_type="application/json",
        ),
    )
    try:
        queries = json.loads(resp.text)["queries"]
    except (json.JSONDecodeError, KeyError, TypeError):
        queries = [question]  # fallback: busca direta
    return queries[:4]


def search(queries: list[str], max_results: int = 5) -> list[dict]:
    seen, sources = set(), []
    for q in queries:
        res = tavily.search(query=q, search_depth="advanced", max_results=max_results)
        for r in res.get("results", []):
            if r["url"] not in seen:
                seen.add(r["url"])
                sources.append(
                    {"title": r["title"], "url": r["url"], "content": r["content"]}
                )
    return sources


def analyze(question: str, sources: list[dict]) -> str:
    context = "\n\n".join(
        f"[{i}] {s['title']} ({s['url']})\n{s['content']}"
        for i, s in enumerate(sources, 1)
    )
    resp = gerar(
        f"Pergunta: {question}\n\nFontes:\n{context}",
        types.GenerateContentConfig(system_instruction=ANALYST_PROMPT, temperature=0.3),
    )
    return resp.text


def research(question: str) -> dict:
    queries = plan_queries(question)
    sources = search(queries)
    if not sources:
        return {"answer": "Não encontrei fontes para essa pergunta.", "queries": queries, "sources": []}
    return {"answer": analyze(question, sources), "queries": queries, "sources": sources}


if __name__ == "__main__":
    out = research(input("Pergunta: "))
    print(out["answer"])
    print("\nFontes:")
    for i, s in enumerate(out["sources"], 1):
        print(f"[{i}] {s['title']} - {s['url']}")