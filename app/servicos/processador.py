import re
from typing import Generator

class ProcessadorDeDocumentos:
    """
    Engine de processamento de texto para pipelines RAG.
    Focado em eficiência de memória utilizando Generators.
    """

    def __init__(self, tamanho_chunk: int = 500, overlap: int = 50):
        """
        Inicializa o processador com regras estritas de fatiamento.
        
        Args:
            tamanho_chunk: Quantidade máxima de palavras por bloco.
            overlap: Quantidade de palavras sobrepostas para manter o contexto semântico.
        """
        if overlap >= tamanho_chunk:
            raise ValueError("Erro de Arquitetura: O overlap deve ser menor que o tamanho do chunk.")
        
        self.tamanho_chunk = tamanho_chunk
        self.overlap = overlap

    def _limpar_texto(self, texto_bruto: str) -> str:
        """
        Método privado de sanitização de dados.
        Remove ruídos e espaços excedentes usando expressões regulares (Regex).
        """
        # Substitui múltiplas quebras de linha ou espaços por um único espaço
        texto_limpo = re.sub(r'\s+', ' ', texto_bruto)
        return texto_limpo.strip()

    def gerar_chunks(self, texto_bruto: str) -> Generator[str, None, None]:
        """
        Fatia textos massivos protegendo a alocação de RAM.
        
        Yields:
            str: O próximo bloco de texto processado.
        """
        texto_limpo = self._limpar_texto(texto_bruto)
        palavras = texto_limpo.split()
        passo = self.tamanho_chunk - self.overlap

        for i in range(0, len(palavras), passo):
            bloco = palavras[i : i + self.tamanho_chunk]
            yield " ".join(bloco)
            
            # Condição de parada tática para evitar iterações vazias
            if i + self.tamanho_chunk >= len(palavras):
                break