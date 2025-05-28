import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import time
import urllib.parse
import re
import os

class ScholarScraperUH:
    def __init__(self):
        self.base_url = "https://scholar.google.com/scholar"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'es-ES,es;q=0.9'
        }
        self.target_articles = 500  # Cantidad objetivo de artículos a recolectar
        self.max_retries = 3
        self.pdf_folder = "PDFs_UH"

    def build_query(self):
        return '"Universidad de La Habana" OR "University of Havana"'

    def extract_article_data(self, result):
        title_tag = result.find('h3', class_='gs_rt')
        title = title_tag.get_text(strip=True) if title_tag else 'Título no disponible'
        
        authors_tag = result.find('div', class_='gs_a')
        authors = authors_tag.get_text(strip=True) if authors_tag else 'Autores no disponibles'

        # Filtrar artículos relevantes
        if ("Universidad de La Habana" in authors or "University of Havana" in authors or
            "Universidad de La Habana" in title or "University of Havana" in title):

            year = self.extract_year(authors)
            link_tag = title_tag.find('a') if title_tag else None
            link = link_tag['href'] if link_tag else '#'

            # Intentar descargar PDF si está disponible
            if link.endswith(".pdf"):
                self.download_pdf(link, title)

            return {
                'Título': title,
                'Autores': authors,
                'Año': year,
                'Enlace': link,
                'Institución': 'Universidad de La Habana'
            }
        else:
            return None

    def extract_year(self, authors_text):
        match = re.search(r'\b(19|20)\d{2}\b', authors_text)
        return match.group(0) if match else 'N/A'

    def download_pdf(self, url, title):
        try:
            if url.endswith(".pdf"):
                safe_title = "".join(c for c in title if c.isalnum() or c in " _-").rstrip()
                filename = os.path.join(self.pdf_folder, f"{safe_title[:80]}.pdf")
                r = requests.get(url, headers=self.headers, timeout=15)
                if r.status_code == 200 and r.headers.get('Content-Type', '').lower().startswith('application/pdf'):
                    with open(filename, 'wb') as f:
                        f.write(r.content)
                    print(f"PDF guardado: {filename}")
                    return True
        except Exception as e:
            print(f"Error al descargar PDF: {e}")
        return False

    def scrape(self):
        articles = []
        page = 0
        session = requests.Session()
        session.headers.update(self.headers)

        # Crear carpeta para PDFs
        os.makedirs(self.pdf_folder, exist_ok=True)

        while len(articles) < self.target_articles:
            params = {
                'q': self.build_query(),
                'start': page * 10,
                'hl': 'es',
                'as_ylo': '2010'
            }

            for attempt in range(self.max_retries):
                try:
                    response = session.get(self.base_url, params=params)
                    response.raise_for_status()

                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = soup.find_all('div', class_='gs_ri')

                    with open(f'resultado_pagina_{page}.html', 'w', encoding='utf-8') as f:
                        f.write(response.text)

                    if not results:
                        print("No se encontraron resultados. Verifica si Google ha bloqueado el scraping.")
                        return articles
                    
                    for result in results:
                        if len(articles) >= self.target_articles:
                            break
                        article = self.extract_article_data(result)
                        if article:
                            articles.append(article)

                    time.sleep(2 if page % 3 == 0 else 5)
                    page += 1
                    break

                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        wait_time = 30 * (attempt + 1)
                        print(f"Bloqueo detectado. Esperando {wait_time} segundos...")
                        time.sleep(wait_time)
                    else:
                        raise

        return articles[:self.target_articles]

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Extracción UH - Google Scholar")
        self.geometry("400x150")
        self.scraper = ScholarScraperUH()
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Guardar resultados en:").pack(pady=5)

        self.btn_folder = tk.Button(self, text="Seleccionar Carpeta", command=self.select_folder)
        self.btn_folder.pack(pady=5)

        self.btn_start = tk.Button(self, text="Iniciar Extracción", command=self.start_scraping)
        self.btn_start.pack(pady=10)

        self.status_label = tk.Label(self, text="")
        self.status_label.pack()

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.scraper.pdf_folder = os.path.join(self.folder_path, "PDFs")
        os.makedirs(self.scraper.pdf_folder, exist_ok=True)

    def start_scraping(self):
        try:
            self.status_label.config(text="Extrayendo artículos...")
            self.update_idletasks()

            articles = self.scraper.scrape()
            if not articles:
                messagebox.showwarning("Aviso", "No se encontraron artículos. Revisa el archivo HTML generado.")
                return

            filename = f"{self.folder_path}/articulos_uh.csv" if hasattr(self, 'folder_path') else "articulos_uh.csv"
            df = pd.DataFrame(articles)
            df.to_csv(filename, index=False, encoding='utf-8-sig')

            messagebox.showinfo("Éxito", f"Se encontraron {len(articles)} artículos\nGuardados en: {filename}\nPDFs en: {self.scraper.pdf_folder}")

        except Exception as e:
            messagebox.showerror("Error", f"Error durante la extracción:\n{str(e)}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
