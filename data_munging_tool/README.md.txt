=========================================
Herramienta Minimalista de Limpieza de Datos
=========================================

Esta es una aplicación de escritorio simple creada en Python que demuestra el poder de la librería Pandas para el "Data Munging" (limpieza y transformación de datos).

La herramienta toma dos archivos de datos "feos" (uno de ventas y uno de productos), los limpia, los combina y exporta dos reportes "limpios" en formato Excel.


--------------------
INSTALACIÓN
--------------------

Esta herramienta requiere las siguientes librerías de Python. Puedes instalarlas usando pip desde tu terminal o consola:

pip install pandas customtkinter openpyxl


--------------------
CÓMO USAR
--------------------

1.  Guarda el script de Python (ej. `data_munging_tool_minimalista.py`) en una carpeta.
2.  Asegúrate de tener tus archivos de datos (ventas y productos) listos.
3.  Abre una terminal o consola, navega a esa carpeta y ejecuta el script:

    python data_munging_tool_minimalista.py

4.  Se abrirá una ventana simple con 3 pasos:
    * Haz clic en "1. Cargar Archivo de Ventas" y selecciona tu archivo.
    * Haz clic en "2. Cargar Archivo de Productos" y selecciona tu archivo.
    * Haz clic en "3. Iniciar Procesamiento y Exportar a Excel".

5.  Espera a que el proceso termine. La consola en la parte inferior de la ventana te mostrará el progreso.
6.  Cuando termine, aparecerá un mensaje de "Éxito".


--------------------
ARCHIVOS DE ENTRADA (Flexibles)
--------------------

La herramienta es agnóstica al formato. Puede leer:
* Archivos .csv
* Archivos .xlsx

*Nota:* La herramienta está diseñada para ser robusta. Puede manejar archivos "feos", como el archivo `productos.xlsx` de la demo que tiene los encabezados en la segunda fila y columnas basura. El script detectará esto y lo corregirá automáticamente.


--------------------
RESULTADOS (Exportación)
--------------------

El script SIEMPRE exportará dos archivos limpios en formato Excel en la misma carpeta donde se ejecutó:

1.  reporte_ventas_por_categoria.xlsx:
    Un reporte agregado que muestra las ventas totales por categoría de producto.

2.  datos_consolidados_limpios.xlsx:
    La base de datos completa y limpia, con los datos de ventas y productos combinados, lista para ser analizada.

*Aviso:* Esta versión minimalista SIEMPRE sobrescribirá estos dos archivos si ya existen.