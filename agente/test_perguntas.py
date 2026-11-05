"""Roda perguntas de teste no agente da Veritas AI e gera um relatório (resultados_teste.md).

Uso: python test_perguntas.py
"""
import re
import time

from agent import research

PERGUNTAS = [
    ("Factual simples", "Qual é a população do Brasil segundo o Censo 2022 do IBGE?"),
    ("Tema polêmico", "A energia nuclear é uma boa opção para o Brasil?"),
    ("Mito conhecido", "É verdade que a Grande Muralha da China é visível do espaço a olho nu?"),
    ("Dado atual", "Qual é a taxa Selic atual definida pelo Copom?"),
    ("Sem evidência", "Qual foi o resultado do estudo de 2024 da Universidade de Marte sobre café?"),
]


def checar(resposta: str, n_fontes: int) -> dict:
    citacoes = [int(n) for n in re.findall(r"\[(\d+)\]", resposta)]
    invalidas = sorted({n for n in citacoes if n < 1 or n > n_fontes})
    return {
        "n_citacoes": len(citacoes),
        "citacoes_invalidas": invalidas,
        "tem_confianca": "nível de confiança" in resposta.lower(),
    }


def main():
    linhas = ["# Resultados do teste - Veritas AI\n"]
    for i, (tipo, pergunta) in enumerate(PERGUNTAS, 1):
        print(f"[{i}/{len(PERGUNTAS)}] {tipo}: {pergunta}")
        inicio = time.time()
        try:
            r = research(pergunta)
        except Exception as e:
            print(f"   ERRO: {e}\n")
            linhas.append(f"## {i}. {tipo}\n**Pergunta:** {pergunta}\n\n**ERRO:** {e}\n")
            continue
        seg = time.time() - inicio
        c = checar(r["answer"], len(r["sources"]))
        print(
            f"   {seg:.1f}s | {len(r['sources'])} fontes | {c['n_citacoes']} citações | "
            f"inválidas: {c['citacoes_invalidas'] or 'nenhuma'} | confiança: {'ok' if c['tem_confianca'] else 'FALTOU'}\n"
        )
        linhas.append(f"## {i}. {tipo}\n**Pergunta:** {pergunta}\n")
        linhas.append(f"**Consultas geradas:** {', '.join(r['queries'])}\n")
        linhas.append(f"**Checagens:** {c}\n")
        linhas.append(f"### Resposta\n{r['answer']}\n")
        linhas.append("### Fontes")
        for n, s in enumerate(r["sources"], 1):
            linhas.append(f"- [{n}] {s['title']} - {s['url']}")
        linhas.append("\n---\n")
        time.sleep(2)  # respiro para os limites de taxa das APIs

    with open("resultados_teste.md", "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    print("Relatório salvo em resultados_teste.md")


if __name__ == "__main__":
    main()