from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.servicos.processador import ProcessadorDeDocumentos
from app.infraestrutura.banco_vetorial import ClienteChromaDB
from app.infraestrutura.cliente_llm import ClienteGroqLLM
from app.servicos.motor_rag import MotorRAG

# Criação do roteador isolado
router = APIRouter(prefix="/conhecimento", tags=["RAG Engine"])

# Inicialização da infraestrutura central
processador_instancia = ProcessadorDeDocumentos()
banco_instancia = ClienteChromaDB()
llm_instancia = ClienteGroqLLM()

# Injeção de dependência no Orquestrador
motor = MotorRAG(processador=processador_instancia, banco_vetorial=banco_instancia, llm=llm_instancia)

# --- DTOs (Data Transfer Objects) para blindagem de entrada ---

class RequisicaoIngestao(BaseModel):
    """Contrato estrito para a injeção de novos textos no sistema."""
    texto: str
    origem: str = "api_direta"

class RequisicaoConsulta(BaseModel):
    """Contrato estrito para requisições de busca vetorial."""
    pergunta: str
    limite: int = 3

# --- Endpoints de Comunicação ---

@router.post("/ingerir")
async def endpoint_ingerir_documento(payload: RequisicaoIngestao):
    """
    Recebe um texto bruto em JSON, processa, fatia e armazena na base vetorial.
    """
    sucesso = motor.ingerir_conteudo(
        texto_bruto=payload.texto,
        metadados_base={"origem": payload.origem}
    )
    
    if not sucesso:
        raise HTTPException(status_code=500, detail="Erro Crítico: Falha na injeção vetorial.")
        
    return {"status": "operante", "mensagem": "Conhecimento processado e indexado com precisão."}

@router.post("/perguntar")
async def endpoint_realizar_consulta(payload: RequisicaoConsulta):
    """
    Executa a busca semântica no banco de dados e retorna os fragmentos 
    mais relevantes para a pergunta enviada.
    """
    contextos = motor.consultar_conhecimento(
        pergunta=payload.pergunta, 
        limite_resultados=payload.limite
    )
    
    return {"resposta": contextos}