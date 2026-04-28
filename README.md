# ⚖️ Legal Process Robot AI

> Automated legal process analysis powered by web scraping + LLMs

## 🚀 Overview

**Legal Process Robot AI** is a REST API designed to automate the analysis of judicial processes from the **TJSP (eSAJ)**.

Given a process number, the API:
- Extracts case data via web scraping
- Processes legal movements using an LLM (**Llama via Groq**)
- Returns a structured and actionable summary

## 🧠 What it delivers

The API transforms raw legal data into:

- 📍 **Current procedural stage**
- 📊 **Case status**
- 💡 **Recommended next action**

All responses are returned in clean, structured **JSON format**, ready for integration with other systems.

## ⚙️ How it works

1. Input a valid process number  
2. Scrape data from TJSP (eSAJ)  
3. Normalize and preprocess case movements  
4. Send data to LLM (Llama via Groq)  
5. Return structured legal insights  

## 🛠️ Tech Stack

- **Python**
- **Playwright** (web scraping)
- **Groq API** (LLM inference)
- **Llama (LLM)**

## 📦 Example Response

```json
{
  "numero_processo": "1000351-41.2020.8.26.0232",
  "fase": "Execução",
  "status": "Aguardando manifestação da parte autora",
  "recomendacao": "Verificar prazo para resposta e peticionar, se necessário"
}
