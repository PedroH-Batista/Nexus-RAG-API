import chromadb
from typing import List, Dict, Any
from app.dominio.interfaces import IVectorDatabase
from app.dominio.entidades import ResultadoBusca

class ClienteChromaDB(IVectorDatabase):
    """
    Implementação concreta da interface IVectorDatabase utilizando ChromaDB.
    Gerencia o ciclo de vida dos embeddings, armazenamento vetorial e buscas semânticas.
    """

    def __init__(self, nome_colecao: str = "nexus_rag_collection", diretorio_persistente: str = "./chroma_data"):
        """
        Inicializa o cliente apontando para um diretório local para persistência de dados.
        Isso garante que os embeddings não sejam apagados quando a API for reiniciada.
        """
        self.cliente = chromadb.PersistentClient(path=diretorio_persistente)
        self.nome_colecao = nome_colecao
        self.colecao = None

    def connect(self) -> None:
        """
        Garante a existência da coleção no ChromaDB. 
        Se a coleção (tabela) não existir, ela é criada. Se existir, é carregada na memória RAM.
        """
        self.colecao = self.cliente.get_or_create_collection(name=self.nome_colecao)
        print(f"[INFRAESTRUTURA] Conexão vetorial estabelecida. Coleção operante: {self.nome_colecao}")

    def add_documents(self, chunks: List[str], metadatas: List[Dict[str, Any]]) -> bool:
        """
        Vetoriza automaticamente e armazena os blocos de texto no banco.
        A assinatura obedece estritamente ao contrato IVectorDatabase.
        """
        if self.colecao is None:
            self.connect()

        # Na engenharia de produção em hiperescala, os IDs devem ser hashes únicos (UUID). 
        # Para a infraestrutura inicial, geramos IDs baseados no lote.
        ids = [f"doc_lote_{i}" for i in range(len(chunks))]

        try:
            self.colecao.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            return True
        except Exception as erro:
            print(f"[ERRO CRÍTICO] Falha na injeção vetorial: {str(erro)}")
            return False

    def similarity_search(self, query: str, top_k: int = 5) -> List[ResultadoBusca]:
        """
        Realiza a busca vetorial cruzando a métrica de distância matemática do ChromaDB
        com a entidade ResultadoBusca do nosso domínio (DataClass).
        """
        if self.colecao is None:
            self.connect()

        resultados_brutos = self.colecao.query(
            query_texts=[query],
            n_results=top_k
        )

        resultados_processados = []
        
        # O ChromaDB retorna dados brutos em listas aninhadas. Precisamos extraí-los com segurança.
        if resultados_brutos['documents'] and resultados_brutos['documents'][0]:
            documentos = resultados_brutos['documents'][0]
            metadados = resultados_brutos['metadatas'][0] if resultados_brutos['metadatas'] else [{}] * len(documentos)
            
            # O ChromaDB usa Distância (quanto menor o número, mais exata é a semântica do texto).
            distancias = resultados_brutos['distances'][0] if resultados_brutos['distances'] else [0.0] * len(documentos)

            for doc, meta, dist in zip(documentos, metadados, distancias):
                # Instanciamos o nosso modelo de dados restrito, bloqueando vazamento de lixo para a API.
                resultado = ResultadoBusca(
                    conteudo=doc,
                    metadados=meta,
                    score_similaridade=dist
                )
                resultados_processados.append(resultado)

        return resultados_processados