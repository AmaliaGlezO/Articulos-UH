import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
import os
import json
from datetime import datetime
import logging
import PyPDF2
from io import BytesIO

class ScholarScraperUH:
    def __init__(self, fireworks_api_key=None):
        self.base_url = "https://scholar.google.com/scholar"
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        self.target_articles = 500
        self.max_retries = 5
        self.request_timeout = 30
        self.session = requests.Session()
        self.session.headers.update({
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        })
        
        # Términos de búsqueda optimizados
        self.keyword_groups = [
            # Tesis y trabajos académicos
            ['"tesis"', '"doctorado"', '"tesis doctoral"', '"tesis de maestría"', '"tesis de licenciatura"'],
            # Facultades principales
            ['"Facultad de Derecho"', '"Facultad de Economía"', '"Facultad de Psicología"', 
             '"Facultad de Biología"', '"Facultad de Física"', '"Facultad de Química"'],
            # Otras unidades académicas
            ['"Facultad de Matemática y Computación"', '"Facultad de Filosofía"', '"Facultad de Comunicación"',
             '"Facultad de Turismo"', '"Facultad de Farmacia"', '"Facultad de Artes y Letras"','"MATCOM'],
            # Institutos y centros
            ['"Centro de Biomateriales"', '"Instituto Superior de Tecnologías"', '"IFAL"', '"INSTEC"']
        ]
        
        # Mapeo de facultades para detección
        self.facultad_map = {
            'derecho': 'Facultad de Derecho',
            'economía': 'Facultad de Economía',
            'psicología': 'Facultad de Psicología',
            'biología': 'Facultad de Biología',
            'física': 'Facultad de Física',
            'química': 'Facultad de Química',
            'matemática': 'Facultad de Matemática y Computación',
            'computación': 'Facultad de Matemática y Computación',
            'filosofía': 'Facultad de Filosofía, Historia y Sociología',
            'historia': 'Facultad de Filosofía, Historia y Sociología',
            'sociología': 'Facultad de Filosofía, Historia y Sociología',
            'comunicación': 'Facultad de Comunicación',
            'turismo': 'Facultad de Turismo',
            'farmacia': 'Facultad de Farmacia y Alimentos',
            'alimentos': 'Facultad de Farmacia y Alimentos',
            'artes': 'Facultad de Artes y Letras',
            'letras': 'Facultad de Artes y Letras',
            'lenguas': 'Facultad de Lenguas Extranjeras',
            'geografía': 'Facultad de Geografía',
            'biomateriales': 'Centro de Biomateriales',
            'instec': 'Instituto Superior de Tecnologías y Ciencias Aplicadas',
            'matcom': 'MATCOM'
        }

        self.fireworks_api_key = fireworks_api_key
        self.fireworks_headers = {
            "Authorization": f"Bearer {fireworks_api_key}",
            "Content-Type": "application/json"
        } if fireworks_api_key else None

    def get_random_user_agent(self):
        return random.choice(self.user_agents)

    def build_query(self, group_index=0):
        base = '"Universidad de La Habana" OR "University of Havana"'
        keywords = " OR ".join(self.keyword_groups[group_index])
        return f"({base}) AND ({keywords})"

    def analyze_with_fireworks(self, text):
        """Usa Fireworks AI para analizar texto y extraer metadatos adicionales"""
        if not self.fireworks_api_key or not text:
            return {}
        
        try:
            # Limitar el texto a los primeros 5000 caracteres para evitar costos altos
            text = text[:5000]
            
            prompt = """Extrae la siguiente información de este texto académico en formato JSON:
            - Temas principales (3-5)
            - Metodología utilizada
            - Hallazgos clave
            - Palabras clave técnicas (5-10)
            - Posible facultad/área de conocimiento
            
            Texto: {text}""".format(text=text)
            
            payload = {
                "model": "accounts/fireworks/models/llama-v2-70b-chat",
                "prompt": prompt,
                "max_tokens": 1000,
                "temperature": 0.3
            }
            
            response = requests.post(
                "https://api.fireworks.ai/inference/v1/completions",
                headers=self.fireworks_headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            # Parsear la respuesta JSON
            result = response.json()
            analysis = json.loads(result['choices'][0]['text'].strip())
            return analysis
            
        except Exception as e:
            logging.error(f"Error en Fireworks AI: {str(e)}")
            return {}

    def extract_pdf_content(self, pdf_url):
        """Extrae texto de un PDF dado su URL"""
        try:
            response = self.session.get(pdf_url, timeout=self.request_timeout)
            response.raise_for_status()
            
            with BytesIO(response.content) as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logging.error(f"Error extrayendo PDF {pdf_url}: {str(e)}")
            return None

    def extract_metadata(self, result):
        try:
            # Extraer título y enlace
            title_tag = result.find('h3', class_='gs_rt')
            title = title_tag.get_text(strip=True) if title_tag else 'Título no disponible'
            link_tag = title_tag.find('a') if title_tag else None
            link = link_tag['href'] if link_tag else ''
            # Notificación en consola
            print(f"Metadatos extraídos de {link}")

            # Identificar tipo de documento
            doc_type = 'Artículo'
            if any(t in title.lower() for t in ['tesis', 'dissertation', 'thesis']):
                doc_type = 'Tesis'
            elif any(t in title.lower() for t in ['conference', 'proceedings', 'congreso']):
                doc_type = 'Conferencia'
            
            # Extraer información de autores y fuente
            authors_tag = result.find('div', class_='gs_a')
            authors_text = authors_tag.get_text(strip=True) if authors_tag else ''
            
            # Extraer año usando múltiples patrones
            year = 'N/A'
            year_patterns = [
                r'\b(19|20)\d{2}\b',
                r'–\s*(\d{4})',
                r'\((\d{4})\)'
            ]
            for pattern in year_patterns:
                match = re.search(pattern, authors_text)
                if match:
                    year = match.group(1) if len(match.groups()) > 0 else match.group(0)
                    break
            
            # Extraer fuente/revista (el texto después del año)
            if year != 'N/A' and authors_text:
                source_parts = authors_text.split(year)
                source = source_parts[-1].strip(' -.,') if len(source_parts) > 1 else ''
            else:
                source = authors_text
            
            # Extraer resumen
            snippet_tag = result.find('div', class_='gs_rs')
            resumen = snippet_tag.get_text(strip=True) if snippet_tag else ''
            
            # Extraer número de citas
            cites_tag = result.find('a', href=re.compile(r'scholar\?cites'))
            cites = re.search(r'\d+', cites_tag.text).group() if cites_tag else '0'
            
            # Extraer enlaces relacionados
            links = {}
            for link_tag2 in result.find_all('a', class_='gs_nph'):
                link_text = link_tag2.get_text(strip=True).lower()
                if 'cite' in link_text:
                    links['citas'] = 'https://scholar.google.com' + link_tag2['href']
                elif 'versions' in link_text:
                    links['versiones'] = 'https://scholar.google.com' + link_tag2['href']
            
            # Detectar idioma
            idioma = 'español' if re.search(r'[áéíóúñ]', title + resumen, re.I) else 'inglés'
            
            # Detectar facultad
            facultad = self.detect_facultad(title + " " + resumen + " " + authors_text)
            
            # Detectar PDF
            pdf_link = ''
            if link_tag and link_tag.find('span', class_='gs_ctg'):
                pdf_link = link
            elif result.find('div', class_='gs_or_ggsm'):
                pdf_tag = result.find('div', class_='gs_or_ggsm').find('a')
                pdf_link = pdf_tag['href'] if pdf_tag else ''
            
            metadata = {
                'Título': title,
                'Tipo Documento': doc_type,
                'Autores': authors_text,
                'Año': year,
                'Fuente': source,
                'Resumen': resumen,
                'Enlace': link,
                'PDF': pdf_link,
                'Citas': cites,
                'Enlaces Relacionados': links,
                'Idioma': idioma,
                'Facultad': facultad,
                'Institución': 'Universidad de La Habana',
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Añadir análisis de Fireworks si hay API key y PDF disponible
            if self.fireworks_api_key and pdf_link:
                pdf_text = self.extract_pdf_content(pdf_link)
                if pdf_text:
                    fireworks_analysis = self.analyze_with_fireworks(pdf_text)
                    metadata['Fireworks_Analysis'] = fireworks_analysis
                    
                    # Actualizar facultad si Fireworks sugiere una mejor
                    if fireworks_analysis.get('Posible facultad/área de conocimiento'):
                        metadata['Facultad'] = fireworks_analysis['Posible facultad/área de conocimiento']
            
            return metadata
            
        except Exception as e:
            logging.error(f"Error extrayendo metadatos: {str(e)}")
            return None
        
    def detect_facultad(self, text):
        text_lower = text.lower()
        for keyword, facultad in self.facultad_map.items():
            if keyword in text_lower:
                return facultad
        return 'Desconocida'

    def handle_captcha(self, response):
        if "Our systems have detected unusual traffic" in response.text:
            logging.warning("CAPTCHA detectado. Necesita intervención manual.")
            return True
        return False

    def scrape_page(self, params, group_index):
        articles = []
        retries = 0
        
        while retries < self.max_retries:
            try:
                self.session.headers['User-Agent'] = self.get_random_user_agent()
                delay = random.uniform(3, 8)
                time.sleep(delay)
                
                response = self.session.get(
                    self.base_url, 
                    params=params,
                    timeout=self.request_timeout
                )
                
                if self.handle_captcha(response):
                    logging.error("Bloqueo por CAPTCHA detectado. Deteniendo scraping.")
                    return []
                
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                
                results = soup.find_all('div', class_='gs_ri')
                if not results:
                    logging.info("No se encontraron resultados para esta consulta")
                    return []
                
                for result in results:
                    metadata = self.extract_metadata(result)
                    if metadata:
                        articles.append(metadata)
                        if len(articles) >= self.target_articles:
                            return articles
                return articles
                
            except requests.exceptions.RequestException as e:
                retries += 1
                wait_time = 10 * retries
                logging.warning(f"Error de red ({str(e)}). Reintento {retries}/{self.max_retries} en {wait_time}s")
                time.sleep(wait_time)
            except Exception as e:
                logging.error(f"Error inesperado: {str(e)}")
                retries += 1
                time.sleep(20)
        logging.error(f"Fallo después de {self.max_retries} intentos")
        return []

    def scrape(self):
        all_articles = []
        group_index = 0
        start_page = 0
        
        try:
            if os.path.exists('progress.txt'):
                with open('progress.txt', 'r') as f:
                    group_index = int(f.readline().strip())
                    start_page = int(f.readline().strip())
                logging.info(f"Reanudando desde grupo {group_index}, página {start_page}")
        except Exception:
            pass
        
        while len(all_articles) < self.target_articles and group_index < len(self.keyword_groups):
            page = start_page
            start_page = 0
            while len(all_articles) < self.target_articles:
                params = {
                    'q': self.build_query(group_index),
                    'start': page * 10,
                    'hl': 'es',
                    'as_ylo': '2000'
                }
                logging.info(f"Scraping: Grupo {group_index+1}/{len(self.keyword_groups)}, Página {page+1}")
                articles = self.scrape_page(params, group_index)
                if not articles:
                    logging.info(f"No se encontraron más artículos para el grupo {group_index}")
                    break
                all_articles.extend(articles)
                with open('progress.txt', 'w') as f:
                    f.write(f"{group_index}\n{page + 1}")
                page += 1
                if len(all_articles) >= self.target_articles:
                    break
            group_index += 1
        if os.path.exists('progress.txt'):
            os.remove('progress.txt')
        return all_articles[:self.target_articles]

    def save_results(self, articles, csv_filename="articulos_uh.csv", json_filename="articulos_uh.json"):
        try:
            if not articles:
                logging.warning("No hay artículos para guardar")
                return False
            df = pd.DataFrame(articles)
            os.makedirs(os.path.dirname(csv_filename) or ".", exist_ok=True)
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            logging.info(f"Archivo guardado: {csv_filename}")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"{timestamp}_{os.path.basename(csv_filename)}")
            df.to_csv(backup_file, index=False, encoding='utf-8-sig')
            logging.info(f"Copia de seguridad guardada: {backup_file}")

            # Guardar también en JSON
            with open(json_filename, 'w', encoding='utf-8') as jf:
                json.dump(articles, jf, ensure_ascii=False, indent=2)
            logging.info(f"Archivo JSON guardado: {json_filename}")
            return True
        except Exception as e:
            logging.error(f"Error guardando resultados: {str(e)}", exc_info=True)
            return False

# Modificación en el main para usar la API key
if __name__ == "__main__":
    print("Iniciando extracción de documentos científicos de la UH...")
    
    # Configura tu API key de Fireworks aquí o déjala como None para no usarla
    FIREWORKS_API_KEY = "fw_3Zn57yCKjDyBFE4TxLmvmnGV"  # o None
    
    scraper = ScholarScraperUH(FIREWORKS_API_KEY)
    articulos = scraper.scrape()
    
    if articulos:
        print(f"\nExtracción completada! Artículos encontrados: {len(articulos)}")
        if scraper.save_results(articulos):
            print("Datos guardados exitosamente en articulos_uh.csv y articulos_uh.json")
            
            # Mostrar ejemplo de análisis de Fireworks si está disponible
            if FIREWORKS_API_KEY:
                print("\nEjemplo de análisis con Fireworks AI:")
                for art in articulos[:2]:  # Mostrar solo 2 ejemplos
                    if 'Fireworks_Analysis' in art:
                        print(f"\nTítulo: {art['Título']}")
                        print("Análisis:")
                        print(json.dumps(art['Fireworks_Analysis'], indent=2, ensure_ascii=False))
        else:
            print("Error al guardar los datos. Ver scraper.log")
