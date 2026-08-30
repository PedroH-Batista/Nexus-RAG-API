import streamlit as st
import requests

# Configuração de Janela
st.set_page_config(page_title="Nexus RAG - UI", layout="centered")
st.title("Terminal Cognitivo: RAG")
st.markdown("Interface tática para extração de dados do banco vetorial.")

# Linha de Comando do Usuário
pergunta = st.text_input("Insira o vetor de busca (Pergunta):")

# Gatilho de Disparo
if st.button("Executar Consulta"):
    if pergunta.strip():
        with st.spinner("Extraindo tensores e processando via LLM..."):
            
            payload = {
                "pergunta": pergunta,
                "limite": 3
            }
            
            try:
                # O Streamlit atira contra a própria API
                resposta = requests.post("http://127.0.0.1:8000/conhecimento/perguntar", json=payload)
                
                # Tratamento do retorno
                if resposta.status_code == 200:
                    dados = resposta.json()
                    st.success("Operação concluída com sucesso.")
                    st.info(f"**Resposta da Inteligência Artificial:**\n\n{dados.get('resposta')}")
                else:
                    st.error(f"Falha de infraestrutura. Código HTTP: {resposta.status_code}")
                    st.json(resposta.json())
                    
            except requests.exceptions.ConnectionError:
                st.error("[ERRO CRÍTICO] O servidor FastAPI (Uvicorn) está offline. Ligue o motor base primeiro.")
    else:
        st.warning("O comando não pode estar vazio. Insira uma pergunta.")