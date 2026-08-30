from pydantic_settings import BaseSettings, SettingsConfigDict

class Configuracao(BaseSettings):
    """
    Gerenciador central de credenciais e variáveis de ambiente.
    Isola a aplicação de chaves hardcoded e garante validação de tipagem em tempo de inicialização.
    """
    # Se esta variável não for encontrada no .env ou no SO, a aplicação recusa a ignição.
    groq_api_key: str 

    # Configuração estrita para leitura do cofre local na fase de desenvolvimento
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instância unificada. O restante do sistema importará apenas este objeto.
config = Configuracao()