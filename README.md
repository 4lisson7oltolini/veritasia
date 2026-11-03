# Veritas AI — Agente de Pesquisa e Análise

Veritas AI é um agente inteligente projetado para realizar pesquisas profundas na internet, coletar evidências de fontes confiáveis e gerar análises imparciais utilizando o poder do Google Gemini e a precisão da Tavily Search.

## Objetivo
Fornecer uma ferramenta profissional para verificação de informações e síntese de conhecimento baseado em fontes reais e atualizadas.

## Tecnologias
- **Linguagem:** [Python 3.12+](https://www.python.org/)
- **IA Generativa:** [Google Gemini API](https://ai.google.dev/) (SDK `google-genai`)
- **Busca Web:** [Tavily Search API](https://tavily.com/)
- **Interface:** [Streamlit](https://streamlit.io/)
- **Ambiente:** `python-dotenv`

## Pré-requisitos
- Python instalado.
- Chave de API do Google AI Studio (Gemini).
- Chave de API da Tavily.

## Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd veritas-ai
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as chaves de API:**
   - Crie um arquivo chamado `.env` na raiz do projeto (use o `.env.example` como base).
   - Adicione suas chaves:
     ```env
     GEMINI_API_KEY=sua_chave_aqui
     TAVILY_API_KEY=sua_chave_aqui
     ```
   - **Nota:** O arquivo `.env` nunca deve ser enviado para o controle de versão.

## Executando Testes
Para validar se as chaves e a conexão com as APIs estão funcionando:
```bash
python test_apis.py
```

## Como iniciar a interface
Inicie o servidor do Streamlit para acessar a interface web:
```bash
streamlit run app.py
```

## Estado Atual
O projeto está na fase de **Fundação**. As conexões com as APIs foram validadas e a estrutura básica da interface está pronta. A lógica do agente de pesquisa será implementada na próxima etapa.
