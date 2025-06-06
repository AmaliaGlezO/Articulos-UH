# Problema:
Las publicaciones científicas de la Universidad de la Habana (UH) forman una red de conocimiento donde autores, documentos y citas interactúan de manera compleja. Sin embargo, no se ha estudiado cómo estas relaciones influyen en la difusión del conocimiento, la colaboración entre investigadores o la estructura de comunidades académicas.

# Objetivo:
Analizar la estructura de redes de coautoría, citaciones y temáticas de los documentos científicos de la UH en Google Scholar, utilizando teoría de grafos para identificar patrones de colaboración, influencia de autores, comunidades temáticas y centralidad de publicaciones clave.

# Posibles enfoques del análisis:

- Red de coautoría: Grafo donde los nodos son autores y las aristas representan colaboraciones.

- Red de citaciones: Grafo dirigido donde los nodos son documentos y las aristas son citas.

- Red temática: Grafo de palabras clave o términos frecuentes para identificar clusters temáticos.

- Métricas de centralidad: Identificar los autores o documentos más influyentes (grado, intermediación, cercanía).


# Objetivo (Programacion):
Desarrollar una aplicación web en Streamlit que permita visualizar y analizar los datos de publicaciones científicas de la UH, incluyendo filtros por año, autor, facultad, citaciones y redes de colaboración, facilitando la extracción de insights académicos.

# Funcionalidades posibles:

- Dashboard general: Estadísticas totales de publicaciones, autores más productivos, años con más actividad.

- Búsqueda y filtrado: Por autor, facultad, año, palabras clave.

- Visualización de redes: Grafos interactivos de coautoría y citaciones.

- Análisis de tendencias: Evolución temporal de temas o colaboraciones.


# Datos que se pueden extraer de cada documento
- Además de título, autores y citas, se puede extraer:

### Metadatos básicos:

- Año de publicación

- Revista o conferencia donde se publicó

- DOI / Enlace al documento

- Resumen (abstract)

### Datos de autores:

- Afiliación (Facultad/Departamento de la UH)

- Posible colaboración interdisciplinaria

- Historial de publicaciones (si hay datos temporales)

### Datos de citación:

- Número de citas recibidas

- Autores/artículos citados (para construir la red de referencias)

- Autores que citan el trabajo (impacto externo)

### Contenido y temática:

- Palabras clave (si están disponibles)

- Análisis de texto (términos frecuentes, temas con NLP)

- Campo de investigación (inferido de revistas o términos clave)

# Ideas Adicionales para Ambos Proyectos
### ARC:

- Detectar "puentes" académicos (autores que conectan facultades).

- Comparar la red de la UH con otras universidades (si hay datos).

- Modelar la difusión de conocimiento usando redes de citas.

### Streamlit:

- Añadir un módulo de "recomendación" (documentos similares).

- Integrar un pequeño análisis de sentimiento en los resúmenes.

- Permitir exportar gráficos y datos en CSV/PDF.