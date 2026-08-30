from typing import List, Dict, Any, Optional
from app.servicos.processador import ProcessadorDeDocumentos
from app.dominio.interfaces import IVectorDatabase, IGeradorLLM

class MotorRAG:
    """
    Orquestrador central do sistema RAG.
    Desacopla a regra de negócio da infraestrutura, coordenando o processamento
    de texto e o armazenamento/busca vetorial.
    """

    def __init__(self, processador: ProcessadorDeDocumentos, banco_vetorial: IVectorDatabase, gerador_llm: IGeradorLLM):
        """
        Injeção de dependência estrita. A classe recebe os componentes de infraestrutura
        e serviços instanciados, garantindo isolamento e facilidade de testes unitários.
        """
        self.processador = processador
        self.banco_vetorial = banco_vetorial
        self.gerador_llm = gerador_llm

    def ingerir_conteudo(self, texto_bruto: str, metadados_base: Optional[Dict[str, Any]] = None) -> bool:
        """
        Recebe o texto bruto, executa o fatiamento de alta performance e ordena 
        a persistência na infraestrutura vetorial.
        """
        if metadados_base is None:
            metadados_base = {}

        # Consome o Generator do processador
        chunks = list(self.processador.gerar_chunks(texto_bruto))
        
        # Replica os metadados para garantir o rastreio de cada fragmento
        metadados = [metadados_base.copy() for _ in chunks]

        # Comanda a injeção na base de dados
        sucesso = self.banco_vetorial.add_documents(chunks=chunks, metadatas=metadados)
        return sucesso

    def consultar_conhecimento(self, pergunta: str, limite_resultados: int = 3) -> str:
        """
        Executa a esteira RAG completa: recupera o contexto matemático vetorial 
        e delega a consolidação ao motor LLM para geração da resposta final.
        """
        resultados = self.banco_vetorial.similarity_search(query=pergunta, top_k=limite_resultados)
        
        # Extrai os textos do modelo de dados ResultadoBusca (DataClass)
        contextos_recuperados = [resultado.conteudo for resultado in resultados]
        
        # Consolidação de blocos para injeção no prompt
        contexto_unificado = "\n\n---\n\n".join(contextos_recuperados)
        
        # O orquestrador aciona a interface do LLM, passando os limites estritos da operação.
        resposta_final = self.gerador_llm.gerar_resposta(
            contexto=contexto_unificado, 
            pergunta=pergunta
        )
        
        return resposta_final