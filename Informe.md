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


# Como se extrajeron los datos: 
Documentos científicos de la Universidad de La Habana en Google Scholar
No es posible listar literalmente “todos” los documentos científicos publicados por la Universidad de La Habana en Google Scholar, ya que la plataforma no permite filtrar directamente por afiliación institucional para obtener un listado exhaustivo en una sola consulta. Sin embargo, a partir de los resultados y perfiles de autores asociados a la Universidad de La Habana, se pueden identificar ejemplos de tesis, doctorados y publicaciones científicas relevantes, así como las palabras clave más útiles para encontrar estos documentos.

Ejemplos de documentos científicos y tesis
A continuación, se muestran ejemplos de publicaciones y tesis asociadas a la Universidad de La Habana, extraídas de perfiles de Google Scholar:

Tesis y doctorados:

“Diagnóstico del proceso de cohesión grupal en contextos escolares” (Facultad de Psicología, Universidad de La Habana. Tesis en opción al grado).

“Con el catalejo al revés… Identidad social de los grupos de la estructura socioclasista cubana” (Tesis de Licenciatura. Facultad de Psicología, Universidad de La Habana).

Artículos científicos y libros:

“Recursos didácticos integradores para facilitar, en la estructura cognoscitiva de los profesores, la formación de conceptos del área de las ciencias naturales en la secundaria” (Universidad de la Habana, 2008).

“La reforma universitaria de 1962: un hito para la educación superior cubana” (Revista Cubana de Educación Superior, 2018).

“Estrategia de superación profesional para la elaboración y publicación de artículos científicos” (Biotempo, 2021).

“Las tecnologías de la información y las comunicaciones en el proyecto educativo de la Universidad Politécnica Salesiana del Ecuador” (Revista Cubana de Educación Superior, 2015).

“Articulaciones teóricas y metodológicas entre los procesos de inclusión-exclusión educativa, cohesión grupal y rendimiento” (Revista de Psicología-Tercera época, 2020).

Palabras clave recomendadas para buscar documentos
Basado en los resultados y en estudios bibliométricos sobre la producción científica de la Universidad de La Habana, las siguientes palabras clave pueden ayudarte a encontrar documentos científicos, tesis y publicaciones asociadas a esta institución en Google Scholar y otras bases de datos:

“Universidad de La Habana”

“tesis Universidad de La Habana”

“doctorado Universidad de La Habana”

“Facultad de [nombre de la facultad] Universidad de La Habana”

“producción científica Universidad de La Habana”

“investigación Universidad de La Habana”

“tesis de licenciatura Universidad de La Habana”

“tesis de maestría Universidad de La Habana”

“tesis doctoral Universidad de La Habana”

“publicaciones Universidad de La Habana”

“tesis psicología Universidad de La Habana”

“tesis ciencias naturales Universidad de La Habana”

“tesis educación Universidad de La Habana”

Además, puedes combinar estas palabras clave con términos específicos de áreas de interés, como “biología”, “química”, “física”, “educación”, “psicología”, “innovación”, “gestión del conocimiento”, etc.

Áreas de mayor productividad científica
Según estudios bibliométricos, las áreas y centros de la Universidad de La Habana con mayor producción científica son:

Facultad de Física

Facultad de Química

Facultad de Biología

Instituto de Materiales y Reactivos

Centro de Biomateriales

Centro de Investigación y Evaluaciones Biológicas

Recomendaciones para la búsqueda
Utiliza Google Scholar y coloca entre comillas “Universidad de La Habana” junto con la palabra clave deseada (por ejemplo: “tesis Universidad de La Habana”).



