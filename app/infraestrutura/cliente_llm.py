from groq import Groq
from app.dominio.interfaces import IGeradorLLM
from app.core.config import config

class ClienteGroqLLM(IGeradorLLM):
    """
    Implementação concreta do motor cognitivo utilizando a infraestrutura Groq (LPUs).
    Garante altíssima performance de inferência consumindo modelos open-source avançados.
    """

    def __init__(self, modelo: str = "openai/gpt-oss-20b"):
        """
        Inicializa o cliente instanciando a SDK oficial. Injeta a chave de segurança 
        carregada e validada em tempo de execução pela camada de configuração (Pydantic).
        """
        # A chave é requisitada do config.py de forma silenciosa e segura
        self.cliente = Groq(api_key=config.groq_api_key)
        self.modelo = modelo

    def gerar_resposta(self, contexto: str, pergunta: str) -> str:
        """
        Constrói o prompt estruturado e comanda a IA a gerar a resposta técnica.
        Aplica bloqueio de alucinação (Temperature 0.0) e restrição estrita de escopo.
        """
        # Engenharia de Prompt: As regras inegociáveis passadas para o cérebro da IA.
        prompt_sistema = (
            "Você é o núcleo cognitivo de um sistema corporativo RAG. "
            "Responda à pergunta do usuário baseando-se ÚNICA e EXCLUSIVAMENTE no contexto fornecido abaixo. "
            "Se a informação para responder à pergunta não estiver presente no contexto, você é OBRIGADO a "
            "responder exatamente com a seguinte frase: "
            "'A informação solicitada não consta no contexto indexado pelo sistema de busca vetorial.' "
            "Não invente, não deduza e não alucine informações além do contexto.\n\n"
            f"CONTEXTO RECUPERADO DO BANCO VETORIAL:\n{contexto}"
        )

        try:
            resposta = self.cliente.chat.completions.create(
                model=self.modelo,
                messages=[
                    {"role": "system", "content": prompt_sistema},
                    {"role": "user", "content": pergunta}
                ],
                temperature=0.0,  # Parâmetro crítico: Remove qualquer criatividade do modelo.
                max_tokens=1024
            )
            
            return resposta.choices[0].message.content

        except Exception as erro:
            print(f"[ERRO CRÍTICO] Falha na comunicação com a API Groq: {str(erro)}")
            return "Falha sistêmica na geração da resposta cognitiva."