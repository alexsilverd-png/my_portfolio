=========================
Demo Web Scraper GUI
=========================

Un sencillo scraper web con interfaz gráfica (GUI) para extraer datos
de páginas web usando selectores CSS.

---
Características
---
* Interfaz gráfica simple (basada en CustomTkinter).
* Extrae datos de cualquier URL usando un selector CSS.
* Muestra los resultados directamente en la aplicación.
* Exporta los resultados a formato .CSV.
* Exporta los resultados a formato Excel (.xlsx).
* Usa 'threading' para evitar que la interfaz se congele durante el proceso.

---
Requisitos
---
* Python 3.x
* customtkinter
* requests
* beautifulsoup4
* openpyxl

---
Instalación
---
Puedes instalar todas las dependencias necesarias usando pip.
Abre tu terminal y ejecuta:

pip install customtkinter requests beautifulsoup4 openpyxl

---
Modo de Uso
---
1. Ejecuta el script de Python (el nombre puede variar):
   python web_scraper.py

2. Pega la URL del sitio web que quieres analizar en el campo "URL del Sitio Web".

3. Introduce el "Selector CSS" para los elementos específicos que quieres extraer.
   (Puedes encontrarlo usando las herramientas de desarrollador de tu navegador,
   con "Inspeccionar elemento").

4. Haz clic en el botón "Iniciar Scrapeo".

5. Los resultados aparecerán en el cuadro de texto.

6. Si el scrapeo fue exitoso, puedes usar los botones "Exportar a .CSV" o
   "Exportar a Excel" para guardar los datos en un archivo.

---
Ejemplo de Prueba (Sitio recomendado)
---
Usa este sitio si quieres verificar que el programa funciona correctamente,
ya que está diseñado para practicar scraping:

* URL del Sitio Web: https://books.toscrape.com/
* Selector CSS: h3 a

Esto debería devolver una lista con todos los títulos de los libros
de la página principal.

---
¡IMPORTANTE! - Advertencia sobre Sitios Modernos
---
Este es un scraper *simple*. NO funcionará en la mayoría de sitios web
comerciales modernos (como Mercado Libre, Amazon, Twitter, Facebook, etc.).

¿Por qué? Esos sitios usan sistemas anti-bots avanzados que detectan
peticiones simples (como las de la librería 'requests') y las bloquean
o devuelven una página de CAPTCHA ("Verifica que no eres un robot").

Además, si un sitio web cambia su diseño (su código HTML), el selector CSS
que usabas dejará de funcionar y tendrás que encontrar el nuevo.

Usa esta herramienta de forma responsable y respeta los términos de servicio
de los sitios web que analizas.