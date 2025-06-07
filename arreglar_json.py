import json
import requests
import time
import spacy
import langdetect
from difflib import SequenceMatcher
from dotenv import load_dotenv
import os

nlp = spacy.load("es_core_news_sm")


load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")


def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def detectar_idioma(texto):
    try:
        return langdetect.detect(texto)
    except:
        return "desconocido"

def buscar_en_scholar(titulo):
    params = {
        "engine": "google_scholar",
        "q": titulo,
        "hl": "es",
        "api_key": SERPAPI_KEY
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        return response.json().get("organic_results", [])
    return []

def extraer_fecha(texto):
    doc = nlp(texto)
    for ent in doc.ents:
        if ent.label_ == "DATE":
            return ent.text
    return ""

def extraer_palabras_clave(texto, num=5):
    doc = nlp(texto)
    palabras = [token.lemma_ for token in doc if token.pos_ in ("NOUN", "PROPN") and not token.is_stop]
    return list(set(palabras))[:num]

def procesar_resultado(resultado):
    resumen = resultado.get("snippet", "")
    fuente = resultado.get("publication_info", {}).get("summary", "")
    link = resultado.get("link", "")
    recursos = resultado.get("resources", [])
    autores = fuente.split("-")[0].strip() if "-" in fuente else fuente

    return {
        "Título": resultado.get("title", ""),
        "Autor(es)": autores,
        "Afiliación": "Universidad de La Habana",  # fijo, con refinamiento posible
        "Resumen": resumen,
        "Palabras clave": extraer_palabras_clave(resumen),
        "Fecha de publicación": extraer_fecha(resumen),
        "Fuente": fuente,
        "Idioma": detectar_idioma(resumen or resultado.get("title", "")),
        "Tipo de documento": "Artículo" if "journal" in fuente.lower() or "revista" in fuente.lower() else "Desconocido",
        "Referencias": "No disponibles en Google Scholar",
        "Licencia/Derechos": "No disponible",
        "Identificadores": {
            "URL": link,
            "PDF": recursos[0].get("link", "") if recursos else ""
        }
    }

# Leer artículos
with open("articulos_uh.json", encoding="utf-8") as f:
    articulos = json.load(f)

resultados = []

for entrada in articulos:
    titulo = entrada.get("Título", "").replace("[CITAS][C]", "").replace("[HTML][HTML]", "").strip()
    print(f"Buscando: {titulo}")
    resultados_scholar = buscar_en_scholar(titulo)

    if resultados_scholar:
        mejor = max(resultados_scholar, key=lambda x: similar(titulo, x.get("title", "")))
        metadatos = procesar_resultado(mejor)
        resultados.append(metadatos)
    else:
        resultados.append({
            "Título": titulo,
            "Autor(es)": entrada.get("Autores", ""),
            "Afiliación": entrada.get("Institución", ""),
            "Resumen": "",
            "Palabras clave": [],
            "Fecha de publicación": entrada.get("Año", ""),
            "Fuente": entrada.get("Fuente", ""),
            "Idioma": entrada.get("Idioma", ""),
            "Tipo de documento": entrada.get("Tipo Documento", ""),
            "Referencias": "No disponibles",
            "Licencia/Derechos": "No disponible",
            "Identificadores": {
                "URL": "",
                "PDF": ""
            }
        })

    time.sleep(3)

# Guardar resultado enriquecido
with open("articulos_enriquecidos_completo.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print("Proceso finalizado. Archivo: articulos_enriquecidos_completo.json")
