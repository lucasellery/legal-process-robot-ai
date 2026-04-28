from playwright.sync_api import sync_playwright
import re

def _parse_numero_processo(numero_processo: str):
    """
    Divide o número unificado CNJ em partes para preencher o formulário do TJSP.
    Formato: NNNNNNN-DD.AAAA.J.TT.OOOO
    Ex: 1000351-41.2020.8.26.0232
      → numeroDigitoAnoUnificado = "1000351-41.2020"
      → foroNumeroUnificado      = "0232"
    """
    # Remove espaços
    numero_processo = numero_processo.strip()

    # Tenta extrair o foro (últimos 4 dígitos após o último ponto)
    match = re.match(
        r"(\d{7}-\d{2}\.\d{4})\.\d\.\d{2}\.(\d{4})", numero_processo
    )
    if match:
        numero_digit_ano = match.group(1)  # ex: "1000351-41.2020"
        foro             = match.group(2)  # ex: "0232"
        return numero_digit_ano, foro

    # Se não casar, devolve tudo no primeiro campo e foro vazio
    return numero_processo, ""


def extrair_movimentacoes(numero_processo: str):
    numero_digit_ano, foro = _parse_numero_processo(numero_processo)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://esaj.tjsp.jus.br/cpopg/open.do", wait_until="networkidle")

        # Preenche o campo principal do número do processo
        page.fill('input[name="numeroDigitoAnoUnificado"]', numero_digit_ano)

        # Preenche o foro (campo separado no formulário do TJSP)
        if foro:
            foro_input = page.query_selector('input[name="foroNumeroUnificado"]')
            if foro_input:
                foro_input.fill(foro)

        # Submete o formulário
        page.click('input[type="submit"]')

        # Aguarda a página de resultado carregar
        try:
            page.wait_for_selector("tr.fundoClaro, tr.fundoEscuro, table.secaoFormBody", timeout=10000)
        except Exception:
            page.wait_for_timeout(5000)

        # ----- DEBUG: mostra o title da página e o primeiro trecho do HTML -----
        print(f"[DEBUG] Title: {page.title()}")
        print(f"[DEBUG] URL: {page.url}")

        # Tenta seletores conhecidos do TJSP (fundoClaro + fundoEscuro)
        rows = page.query_selector_all("tr.fundoClaro, tr.fundoEscuro")

        if not rows:
            # Fallback: tenta linhas de qualquer tabela dentro da área de movimentações
            rows = page.query_selector_all("#tabelaTodasMovimentacoes tr")

        if not rows:
            # Último recurso: todas as <tr> que tenham conteúdo de texto relevante
            rows = page.query_selector_all("table tr")
            rows = [r for r in rows if len(r.inner_text().strip()) > 10]

        print(f"[DEBUG] Linhas encontradas: {len(rows)}")

        movimentacoes = []
        for row in rows:
            texto = row.inner_text().strip()
            if texto:
                movimentacoes.append(texto)

        browser.close()

    return movimentacoes

# if __name__ == "__main__":
#     movs = extrair_movimentacoes("1000351-41.2020.8.26.0232")
#     for i, m in enumerate(movs, 1):
#         print(f"\n--- Movimentação {i} ---")
#         print(m)

#     if not movs:
#         print("Nenhuma movimentação encontrada.")
