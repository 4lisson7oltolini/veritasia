import streamlit as st

from agente.agent import research

st.set_page_config(page_title="Veritas AI", page_icon="🔍")


def render_result(result: dict) -> None:
    st.markdown(result["answer"])

    with st.expander("Consultas usadas na busca"):
        for q in result["queries"]:
            st.markdown(f"- {q}")

    with st.expander(f"Fontes ({len(result['sources'])})"):
        for i, s in enumerate(result["sources"], 1):
            st.markdown(f"**[{i}]** [{s['title']}]({s['url']})")


def main():
    st.title("🔍 Projeto Veritas AI")
    st.subheader("Agente de Pesquisa e Análise de Evidências")

    st.markdown("""
    Bem-vindo ao **Veritas AI**. Este projeto utiliza Inteligência Artificial e buscas em tempo real
    para fornecer análises baseadas em evidências.
    """)

    if "history" not in st.session_state:
        st.session_state.history = []  # lista de {"query": ..., "result": ...}

    query = st.text_input(
        "O que você deseja pesquisar?",
        placeholder="Ex: Impacto da energia solar no Brasil",
    )

    if st.button("Iniciar Pesquisa"):
        if not query.strip():
            st.error("Por favor, insira uma pergunta ou tópico para pesquisar.")
        else:
            with st.spinner("Pesquisando e analisando as fontes..."):
                try:
                    result = research(query.strip())
                except Exception as e:
                    st.error(f"Erro durante a pesquisa: {e}")
                else:
                    st.session_state.history.insert(0, {"query": query.strip(), "result": result})
                    st.success(f"Pesquisa concluída: **{query.strip()}**")
                    render_result(result)

    # Histórico da sessão (some ao fechar a aba)
    if st.session_state.history:
        with st.sidebar:
            st.header("Histórico da sessão")
            for item in st.session_state.history:
                with st.expander(item["query"]):
                    render_result(item["result"])

    with st.expander("Sobre o projeto"):
        st.write("""
        - **Tecnologias:** Python, Streamlit, Google Gemini, Tavily.
        - **Objetivo:** Facilitar a verificação de fatos e pesquisa profunda.
        - **Estado Atual:** Agente de pesquisa integrado (planejamento de buscas, coleta de fontes e análise).
        """)


if __name__ == "__main__":
    main()