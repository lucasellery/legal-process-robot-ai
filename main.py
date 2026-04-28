from fastapi import FastAPI
from pydantic import BaseModel
from service import analisar_processo
from scraper import extrair_movimentacoes

app = FastAPI()

class ProcessInputNumber(BaseModel):
  numero_processo: str
  
@app.post("/analisar-processo")
def analyse_real_process(input: ProcessInputNumber):
  try:
    movimentacoes_lista = extrair_movimentacoes(input.numero_processo)

    if not movimentacoes_lista:
      return {
        "erro": "Nenhuma movimentação encontrada"
      }

    # Limita às últimas 30 movimentações (mais recentes e relevantes)
    movimentacoes_recentes = movimentacoes_lista[-30:]
    movimentacoes_texto = "\n".join(movimentacoes_recentes)

    # Limita o texto a 3000 caracteres para não estourar o limite de tokens
    if len(movimentacoes_texto) > 3000:
        movimentacoes_texto = movimentacoes_texto[-3000:]

    result = analisar_processo(movimentacoes_texto)
    
    print("Movimentações capturadas:", movimentacoes_lista)

    return {
      "numero_processo": input.numero_processo,
      "movimentacoes": movimentacoes_lista,
      "analise": result
    }

  except Exception as e:
    return {
      "erro": "Falha ao processar",
      "detalhes": str(e)
    }

@app.get("/")
def home():
  return {
    "message": "API do Robô jurídico rodando 🚀"
  }
