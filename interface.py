import streamlit as st
import requests
import PyPDF2

# Configuração de Janela
st.set_page_config(page_title="Nexus RAG - UI", layout="centered")
st.title("Terminal Cognitivo: RAG")
st.markdown("Interface tática para ingestão e extração de dados do banco vetorial.")

# --- MÓDULO DE INGESTÃO (SIDEBAR) ---
st.sidebar.header("Injeção de Conhecimento")
st.sidebar.markdown("Armamento do banco vetorial via PDF.")
arquivo_pdf = st.sidebar.file_uploader("Carregar documento tático", type=["pdf"])

if st.sidebar.button("Processar e Ingerir"):
    if arquivo_pdf is not None:
        with st.spinner("Extraindo texto e vetorizando (ChromaDB)..."):
            try:
                # Extração de texto em memória (sem salvar no disco)
                leitor = PyPDF2.PdfReader(arquivo_pdf)
                texto_extraido = ""
                for pagina in leitor.pages:
                    texto = pagina.extract_text()
                    if texto:
                        texto_extraido += texto + "\n"
                
                if not texto_extraido.strip():
                    st.sidebar.error("Falha: O PDF está vazio ou é baseado em imagens (sem texto selecionável).")
                else:
                    # Montagem da carga útil para a rota existente
                    payload = {
                        "texto": texto_extraido,
                        "origem": arquivo_pdf.name
                    }
                    
                    # Disparo contra a API Back-end
                    resposta = requests.post("http://127.0.0.1:8000/conhecimento/ingerir", json=payload)
                    
                    if resposta.status_code == 200:
                        st.sidebar.success(f"[{arquivo_pdf.name}] indexado com sucesso.")
                    else:
                        st.sidebar.error(f"Falha na API. Código HTTP: {resposta.status_code}")
                        
            except Exception as e:
                st.sidebar.error(f"Erro crítico no processamento do arquivo: {str(e)}")
    else:
        st.sidebar.warning("Nenhum arquivo selecionado para injeção.")

# --- MÓDULO DE CONSULTA (MAIN) ---
st.markdown("---")
pergunta = st.text_input("Insira o vetor de busca (Pergunta):")

if st.button("Executar Consulta"):
    if pergunta.strip():
        with st.spinner("Extraindo tensores e processando via LLM..."):
            payload = {
                "pergunta": pergunta,
                "limite": 3
            }
            
            try:
                resposta = requests.post("http://127.0.0.1:8000/conhecimento/perguntar", json=payload)
                
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