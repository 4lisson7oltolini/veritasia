import streamlit as st

st.set_page_config(page_title="Veritas AI", page_icon="🔍")

def main():
    st.title("🔍 Projeto Veritas AI")
    st.subheader("Agente de Pesquisa e Análise de Evidências")
    
    st.markdown("""
    Bem-vindo ao **Veritas AI**. Este projeto utiliza Inteligência Artificial e buscas em tempo real 
    para fornecer análises baseadas em evidências.
    """)
    
    # Campo de pesquisa
    query = st.text_input("O que você deseja pesquisar?", placeholder="Ex: Impacto da energia solar no Brasil")
    
    if st.button("Iniciar Pesquisa"):
        if query:
            st.info(f"Iniciando pesquisa sobre: **{query}**")
            st.warning("A aplicação ainda está em fase de implementação. O agente de pesquisa será integrado em breve.")
        else:
            st.error("Por favor, insira uma pergunta ou tópico para pesquisar.")

    with st.expander("Sobre o projeto"):
        st.write("""
        - **Tecnologias:** Python, Streamlit, Google Gemini, Tavily.
        - **Objetivo:** Facilitar a verificação de fatos e pesquisa profunda.
        - **Estado Atual:** Fundação e validação de APIs.
        """)

if __name__ == "__main__":
    main()
