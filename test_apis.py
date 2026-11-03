import os
import sys
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai
from google.genai import types

def test_tavily():
    print("\n--- Testando Tavily Search API ---")
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("ERRO: TAVILY_API_KEY não encontrada no arquivo .env")
        return False
    
    try:
        client = TavilyClient(api_key=api_key)
        print("Iniciando pesquisa: 'site:gov.br energia solar Brasil'...")
        response = client.search(query="site:gov.br energia solar Brasil", max_results=3)
        
        results = response.get('results', [])
        if not results:
            print("AVISO: Nenhun resultado retornado pela Tavily.")
            return False
            
        for i, res in enumerate(results, 1):
            print(f"{i}. {res.get('title')} ({res.get('url')})")
        
        print("SUCESSO: Tavily integrada corretamente.")
        return True
    except Exception as e:
        print(f"ERRO ao testar Tavily: {str(e)}")
        return False

def test_gemini():
    print("\n--- Testando Google Gemini API ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERRO: GEMINI_API_KEY não encontrada no arquivo .env")
        return False
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Tenta listar modelos para verificar conectividade e disponibilidade
        print("Verificando modelos disponíveis...")
        available_models = []
        try:
            for m in client.models.list():
                if 'generateContent' in m.supported_generation_methods:
                    available_models.append(m.name)
        except Exception as list_err:
            print(f"Aviso ao listar modelos: {list_err}")

        # Tenta usar um modelo comum se a lista falhar ou estiver vazia
        model_name = "gemini-1.5-flash"
        if available_models:
            # Prefere flash por ser mais rápido/barato para teste
            flash_models = [m for m in available_models if "flash" in m]
            if flash_models:
                model_name = flash_models[0]
            else:
                model_name = available_models[0]
        
        print(f"Usando modelo: {model_name}")
        response = client.models.generate_content(
            model=model_name,
            contents="Olá! Responda apenas com: 'Gemini Online'."
        )
        
        if response and response.text:
            print(f"Resposta: {response.text.strip()}")
            print("SUCESSO: Gemini integrado corretamente.")
            return True
        else:
            print("ERRO: Resposta vazia do Gemini.")
            return False
            
    except Exception as e:
        # Tratamento de erro detalhado sem expor a chave
        err_msg = str(e).lower()
        if "api_key_invalid" in err_msg or "403" in err_msg:
            print("ERRO: Chave de API inválida ou sem permissão.")
        elif "quota" in err_msg or "429" in err_msg:
            print("ERRO: Limite de requisições ou cota esgotada.")
        elif "connection" in err_msg or "timeout" in err_msg:
            print("ERRO: Falha de conexão ou timeout.")
        else:
            print(f"ERRO ao testar Gemini: {str(e)}")
        return False

def main():
    load_dotenv()
    
    tavily_ok = test_tavily()
    gemini_ok = test_gemini()
    
    print("\n" + "="*30)
    print("RESUMO DOS TESTES")
    print(f"Tavily API: {'[OK]' if tavily_ok else '[FALHA]'}")
    print(f"Gemini API: {'[OK]' if gemini_ok else '[FALHA]'}")
    print("="*30)
    
    if not (tavily_ok and gemini_ok):
        sys.exit(1)

if __name__ == "__main__":
    main()
