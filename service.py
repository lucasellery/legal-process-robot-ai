from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from scraper import extrair_movimentacoes

# Carrega variáveis
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def limpar_json(content: str) -> str:
    # remove ```json e ```
    content = content.replace("```json", "")
    content = content.replace("```", "")
    return content.strip()


def analisar_processo(movimentacoes: str) -> dict:
    prompt_sistema = """
Você é um assistente jurídico especializado em análise de processos.

Analise as movimentações e responda APENAS em JSON com:

- resumo: explicação simples do andamento
- fase:
    - inicial → início do processo
    - intermediaria → ainda em andamento
    - final → pronto para decisão ou encerramento
- status:
    - aguardando_sentenca
    - em_andamento
    - encerrado
- recomendacao: ação sugerida

REGRAS IMPORTANTES:
- Se houver "conclusos para sentença", a fase é "final"
- Se já houve sentença, status é "encerrado"
- Seja objetivo

NÃO escreva nada fora do JSON.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": f"Movimentações:\n{movimentacoes}"}
        ]
    )

    content = response.choices[0].message.content
    
    content_limpo = limpar_json(content)

    try:
        return json.loads(content_limpo)
    except json.JSONDecodeError:
        return {
            "erro": "Resposta não veio em JSON válido",
            "resposta_bruta": content
        }

if __name__ == "__main__":

  testes = [
      {
          "nome": "Processo inicial",
          "movimentacoes": """
          - Petição inicial protocolada
          """
      },
      {
          "nome": "Processo em andamento",
          "movimentacoes": """
          - Petição inicial protocolada
          - Réu citado
          - Contestação apresentada
          """
      },
      {
          "nome": "Próximo de sentença",
          "movimentacoes": """
          - Petição inicial protocolada
          - Réu citado
          - Contestação apresentada
          - Autos conclusos para sentença
          """
      },
  ]

  for teste in testes:
      print("\n==============================")
      print(f"🧪 Teste: {teste['nome']}")
      print("==============================")

      resultado = analisar_processo(teste["movimentacoes"])

      print("\n📥 Input:")
      print(teste["movimentacoes"])

      print("\n📤 Output JSON:")
      print(resultado)
