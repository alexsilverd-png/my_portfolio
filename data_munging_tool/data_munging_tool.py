import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import threading
import unicodedata

# Configuración de la apariencia de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class DataMungingApp(ctk.CTk):
    
    def __init__(self):
        super().__init__()

        # --- Configuración de la Ventana Principal ---
        self.title("Demo de Funcionalidad Total (Pandas)")
        self.geometry("700x700") # Un poco más alta para las nuevas opciones

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1) # Fila 3 es ahora el log

        self.sales_file_path = ""
        self.products_file_path = ""
        
        # --- Frame de Selección de Archivos ---
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.file_frame.grid_columnconfigure(1, weight=1)

        # 1. Archivo de Ventas (CSV o Excel)
        self.btn_sales = ctk.CTkButton(self.file_frame, text="1. Cargar Archivo de Ventas", command=self.select_sales_file)
        self.btn_sales.grid(row=0, column=0, padx=10, pady=10)
        
        self.lbl_sales = ctk.CTkLabel(self.file_frame, text="Ningún archivo (csv o xlsx)", text_color="gray")
        self.lbl_sales.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # 2. Archivo de Productos (CSV o Excel)
        self.btn_products = ctk.CTkButton(self.file_frame, text="2. Cargar Archivo de Productos", command=self.select_products_file)
        self.btn_products.grid(row=1, column=0, padx=10, pady=10)
        
        self.lbl_products = ctk.CTkLabel(self.file_frame, text="Ningún archivo (csv o xlsx)", text_color="gray")
        self.lbl_products.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # --- Frame de Opciones y Ejecución ---
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.options_frame.grid_columnconfigure(1, weight=1)
        
        # 3. Opción de Formato de Salida
        self.export_label = ctk.CTkLabel(self.options_frame, text="3. Formato de Salida:")
        self.export_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        
        self.export_format_var = ctk.StringVar(value="Excel")
        self.export_switch = ctk.CTkSegmentedButton(self.options_frame,
                                                    values=["Excel", "CSV"],
                                                    variable=self.export_format_var)
        self.export_switch.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # 4. Opción de Sobrescribir
        self.chk_overwrite = ctk.CTkCheckBox(self.options_frame, text="Sobrescribir reportes existentes")
        self.chk_overwrite.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="w")
        
        # 5. Botón de Ejecución
        self.run_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.run_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.run_frame.grid_columnconfigure(0, weight=1)
        
        self.btn_run = ctk.CTkButton(self.run_frame, text="4. Iniciar Procesamiento", 
                                      command=self.start_processing_thread, font=("", 14, "bold"), height=40)
        self.btn_run.grid(row=0, column=0, padx=0, pady=0, sticky="ew")

        # --- Consola de Salida / Log ---
        self.log_textbox = ctk.CTkTextbox(self, state="disabled", wrap="word", font=("", 13))
        self.log_textbox.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")


    def log(self, message):
        """ Escribe un mensaje en la consola de la GUI de forma segura. """
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"{message}\n")
        self.log_textbox.configure(state="disabled")
        self.log_textbox.see("end")

    def get_filetypes(self):
        """ Devuelve los tipos de archivo permitidos (CSV y Excel). """
        return [
            ("Archivos de Datos", "*.csv *.xlsx"),
            ("Archivos CSV", "*.csv"),
            ("Archivos Excel", "*.xlsx"),
            ("Todos los archivos", "*.*")
        ]

    def select_sales_file(self):
        """ Abre un diálogo para seleccionar el archivo de ventas (CSV o Excel). """
        file_path = filedialog.askopenfilename(
            title="Selecciona el archivo de ventas",
            filetypes=self.get_filetypes()
        )
        if file_path:
            self.sales_file_path = file_path
            self.lbl_sales.configure(text=os.path.basename(file_path), text_color="white")
            self.log(f"Archivo de Ventas cargado: {file_path}")

    def select_products_file(self):
        """ Abre un diálogo para seleccionar el archivo de productos (CSV o Excel). """
        file_path = filedialog.askopenfilename(
            title="Selecciona el archivo de productos",
            filetypes=self.get_filetypes()
        )
        if file_path:
            self.products_file_path = file_path
            self.lbl_products.configure(text=os.path.basename(file_path), text_color="white")
            self.log(f"Archivo de Productos cargado: {file_path}")

    def start_processing_thread(self):
        """ Inicia el procesamiento en un hilo separado para no congelar la GUI. """
        self.btn_run.configure(state="disabled", text="Procesando...")
        
        sales_file = self.sales_file_path
        products_file = self.products_file_path
        overwrite = self.chk_overwrite.get() == 1
        export_format = self.export_format_var.get() # Nueva opción
        
        processing_thread = threading.Thread(
            target=self.run_processing,
            args=(sales_file, products_file, overwrite, export_format) # Argumento añadido
        )
        processing_thread.start()

    def run_processing(self, sales_path, products_path, overwrite, export_format):
        """ Contiene toda la lógica de Pandas para procesar los datos. """
        try:
            self.log("\n--- INICIANDO PROCESO ---")
            if not sales_path or not products_path:
                raise ValueError("Debes seleccionar ambos archivos (ventas y productos).")

            # --- PASO 1: Cargar los datos (Lógica flexible) ---
            self.log("PASO 1: Cargando datos 'feos'...")
            
            # 1a. Cargar archivo de ventas
            self.log(f"  > Leyendo '{os.path.basename(sales_path)}'...")
            sales_ext = os.path.splitext(sales_path)[1].lower()
            if sales_ext == '.csv':
                df_ventas = pd.read_csv(sales_path)
            elif sales_ext in ['.xlsx', '.xls']:
                df_ventas = pd.read_excel(sales_path)
            else:
                raise ValueError(f"Formato de ventas no soportado: {sales_ext}")
            
            # 1b. Cargar archivo de productos
            self.log(f"  > Leyendo '{os.path.basename(products_path)}'...")
            products_ext = os.path.splitext(products_path)[1].lower()
            if products_ext == '.csv':
                df_productos = pd.read_csv(products_path)
            elif products_ext in ['.xlsx', '.xls']:
                # Aplicamos la lógica inteligente SOLO si es un Excel
                df_productos_raw = pd.read_excel(products_path)
                detected_cols = list(df_productos_raw.columns)
                if (len(detected_cols) >= 3 and
                    'Unnamed: 0' in detected_cols[0] and 
                    detected_cols[1] == 'A' and 
                    detected_cols[2] == 'B'):
                    self.log("    > Formato 'feo' de Excel detectado. Re-leyendo...")
                    df_productos = pd.read_excel(products_path, header=1, usecols="B,C")
                else:
                    df_productos = df_productos_raw # Es un Excel limpio
            else:
                raise ValueError(f"Formato de productos no soportado: {products_ext}")
            
            self.log("  > Archivos cargados con éxito.")

            # --- PASO 2: Limpieza de Datos (Cleaning) ---
            self.log("PASO 2: Limpiando datos de ventas...")
            df_limpio = df_ventas.copy()

            self.log("  > Manejando valores nulos...")
            initial_rows = len(df_limpio)
            df_limpio.dropna(subset=['Cantidad'], inplace=True)
            self.log(f"    > {initial_rows - len(df_limpio)} filas eliminadas por 'Cantidad' nula.")
            df_limpio['Region'] = df_limpio['Region'].fillna('Desconocida')

            self.log("  > Corrigiendo tipos de datos (Precio, Cantidad)...")
            precio_col = next((col for col in df_limpio.columns if 'precio' in col.lower()), None)
            if not precio_col:
                raise ValueError("No se encontró una columna de 'Precio' en el CSV de ventas.")
            
            df_limpio[precio_col] = df_limpio[precio_col].astype(str).str.replace('$', '', regex=False).str.strip()
            df_limpio[precio_col] = pd.to_numeric(df_limpio[precio_col], errors='coerce')
            df_limpio['Cantidad'] = pd.to_numeric(df_limpio['Cantidad'], errors='coerce')

            self.log("  > Estandarizando texto (Mayúsculas/minúsculas)...")
            df_limpio['Producto'] = df_limpio['Producto'].str.capitalize()
            df_limpio['Region'] = df_limpio['Region'].str.strip().str.capitalize()
            
            df_limpio.dropna(subset=[precio_col, 'Cantidad'], inplace=True)
            self.log("  > Limpieza de tipos completada.")

            # --- PASO 3: Transformación ---
            self.log("PASO 3: Creando columna 'Venta_Total'...")
            df_limpio['Venta_Total'] = df_limpio[precio_col] * df_limpio['Cantidad']

            # --- PASO 4: Combinar Datos (Merging) ---
            self.log("PASO 4: Combinando ventas con categorías de productos...")
            
            def normalize_text(text):
                if text is None: return ""
                text = str(text).lower()
                return "".join(c for c in unicodedata.normalize('NFD', text) 
                               if unicodedata.category(c) != 'Mn')

            normalized_cols = {normalize_text(col): col for col in df_productos.columns}
            prod_col_nombre_key = next((key for key in normalized_cols if 'nombre' in key), None)
            prod_col_cat_key = next((key for key in normalized_cols if 'categoria' in key), None)
            prod_col_nombre = normalized_cols.get(prod_col_nombre_key)
            prod_col_cat = normalized_cols.get(prod_col_cat_key)
            
            if not prod_col_nombre or not prod_col_cat:
                raise ValueError(f"No se pudo encontrar 'nombre' o 'categoria' en el archivo de productos. Columnas detectadas: {list(df_productos.columns)}")

            self.log(f"  > Columna de producto detectada: '{prod_col_nombre}'")
            self.log(f"  > Columna de categoría detectada: '{prod_col_cat}'")

            df_final = pd.merge(df_limpio, df_productos, left_on='Producto', right_on=prod_col_nombre, how='left')
            df_final[prod_col_cat] = df_final[prod_col_cat].fillna('Sin Categoría')

            # --- PASO 5: Generar Reportes Limpios ---
            self.log("PASO 5: Generando reportes agregados...")
            reporte_categorias = df_final.groupby(prod_col_cat).agg(
                Ingresos_Totales=('Venta_Total', 'sum'),
                Cantidad_Vendida=('Cantidad', 'sum')
            ).sort_values(by='Ingresos_Totales', ascending=False)

            # --- PASO 6: Exportar (Lógica flexible) ---
            self.log(f"PASO 6: Exportando reportes en formato {export_format}...")
            
            if export_format == "Excel":
                reporte_agregado_file = "reporte_ventas_por_categoria.xlsx"
                datos_limpios_file = "datos_consolidados_limpios.xlsx"
                
                # Chequeo de sobrescritura
                if not overwrite and (os.path.exists(reporte_agregado_file) or os.path.exists(datos_limpios_file)):
                    raise PermissionError(f"Archivos .xlsx ya existen. Habilite 'Sobrescribir'.")
                
                reporte_categorias.to_excel(reporte_agregado_file)
                df_final.to_excel(datos_limpios_file, index=False)
                
            else: # Formato CSV
                reporte_agregado_file = "reporte_ventas_por_categoria.csv"
                datos_limpios_file = "datos_consolidados_limpios.csv"

                # Chequeo de sobrescritura
                if not overwrite and (os.path.exists(reporte_agregado_file) or os.path.exists(datos_limpios_file)):
                    raise PermissionError(f"Archivos .csv ya existen. Habilite 'Sobrescribir'.")

                reporte_categorias.to_csv(reporte_agregado_file)
                df_final.to_csv(datos_limpios_file, index=False)

            self.log(f"  > Reporte agregado guardado en: {reporte_agregado_file}")
            self.log(f"  > Datos limpios guardados en: {datos_limpios_file}")

            self.log("\n--- ¡PROCESO COMPLETADO CON ÉXITO! ---")
            messagebox.showinfo("Éxito", f"Proceso finalizado. Archivos exportados como {export_format}.")

        except Exception as e:
            self.log(f"\n--- ERROR CRÍTICO ---")
            self.log(f"El proceso falló: {str(e)}")
            self.log("------------------------")
            messagebox.showerror("Error en el Proceso", f"Ocurrió un error:\n{e}")
            
        finally:
            self.btn_run.configure(state="normal", text="4. Iniciar Procesamiento")

# --- Bloque principal para ejecutar la aplicación ---
if __name__ == "__main__":
    app = DataMungingApp()
    app.mainloop()