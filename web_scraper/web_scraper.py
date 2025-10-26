

import tkinter
import customtkinter
import requests
from bs4 import BeautifulSoup
import threading
import csv  # Para exportar a CSV
from openpyxl import Workbook  # Para exportar a Excel
from tkinter import filedialog  # Para el diálogo de "Guardar como..."

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Demo Web Scraper GUI")
        self.geometry("700x550") # Un poco más alto

        customtkinter.set_appearance_mode("System")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Creación de Widgets ---

        # 1. URL
        self.label_url = customtkinter.CTkLabel(self, text="URL del Sitio Web:")
        self.label_url.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        self.entry_url = customtkinter.CTkEntry(self, placeholder_text="https://ejemplo.com")
        self.entry_url.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")

        # 2. Selector
        self.label_selector = customtkinter.CTkLabel(self, text="Selector CSS:")
        self.label_selector.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.entry_selector = customtkinter.CTkEntry(self, placeholder_text="Ej: h2 (para todos los títulos h2)")
        self.entry_selector.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # 3. Botón de Scrapeo
        self.scrape_button = customtkinter.CTkButton(self, text="Iniciar Scrapeo", command=self.iniciar_proceso_scrapeo)
        self.scrape_button.grid(row=3, column=1, padx=20, pady=10, sticky="e")
        
        # 4. Etiqueta de Estado
        self.status_label = customtkinter.CTkLabel(self, text="Estado: Esperando...", text_color="gray")
        self.status_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        # 5. Cuadro de Resultados
        self.results_textbox = customtkinter.CTkTextbox(self, width=250)
        self.results_textbox.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="nsew")
        self.results_textbox.configure(state="disabled")

        # --- Botones de Exportación ---
        
        # Un 'Frame' para agrupar los botones de exportación
        self.export_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.export_frame.grid(row=4, column=0, columnspan=2, pady=(0, 15), sticky="ew")
        self.export_frame.grid_columnconfigure((0, 1), weight=1) # Centrar botones

        self.export_csv_button = customtkinter.CTkButton(self.export_frame, text="Exportar a .CSV", command=self.exportar_a_csv, state="disabled")
        self.export_csv_button.grid(row=0, column=0, padx=(0, 10), sticky="e")
        
        self.export_excel_button = customtkinter.CTkButton(self.export_frame, text="Exportar a Excel (.xlsx)", command=self.exportar_a_excel, state="disabled")
        self.export_excel_button.grid(row=0, column=1, padx=(10, 0), sticky="w")
        
        # Almacén para los datos estructurados
        self.lista_resultados = []

    def iniciar_proceso_scrapeo(self):
        url = self.entry_url.get()
        selector = self.entry_selector.get()

        if not url or not selector:
            self.actualizar_estado("Error: La URL y el Selector son requeridos.", "red")
            return

        self.scrape_button.configure(state="disabled", text="Scrapeando...")
        self.actualizar_estado("Procesando...", "gray")
        self.actualizar_resultados("")
        
        # Deshabilitar botones y limpiar datos antiguos
        self.habilitar_botones_exportar(False)
        self.lista_resultados.clear()

        scrape_thread = threading.Thread(target=self.realizar_scrapeo, args=(url, selector), daemon=True)
        scrape_thread.start()

    def realizar_scrapeo(self, url, selector):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }
            
            self.after(0, self.actualizar_estado, "1/3: Descargando HTML...", "white")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            self.after(0, self.actualizar_estado, "2/3: Analizando HTML...", "white")
            soup = BeautifulSoup(response.text, 'html.parser')

            self.after(0, self.actualizar_estado, "3/3: Extrayendo datos...", "white")
            elementos_encontrados = soup.select(selector)

            if not elementos_encontrados:
                self.after(0, self.actualizar_estado, "Completado: No se encontraron elementos con ese selector.", "yellow")
                return
            
            # Limpio la lista (otra vez xD)
            self.lista_resultados.clear()
            
            # Creo una lista de texto para la GUI
            resultados_para_gui = [] 

            for i, elem in enumerate(elementos_encontrados):
                texto = elem.get_text(strip=True)
                if texto:
                    # Añado datos ESTRUCTURADOS a la lista de la clase
                    self.lista_resultados.append([i + 1, texto])
                    # Añado datos FORMATEADOS para el cuadro de texto
                    resultados_para_gui.append(f"{i+1}. {texto}")

            # Unir todos los resultados en un solo string para la GUI
            texto_final = "\n\n".join(resultados_para_gui)

            # Llamar a la función que actualiza y habilita botones
            self.after(0, self.actualizar_gui_con_exito, texto_final, len(self.lista_resultados))

        except requests.exceptions.RequestException as e:
            self.after(0, self.actualizar_estado, f"Error de Red: {e}", "red")
        except Exception as e:
            self.after(0, self.actualizar_estado, f"Error Inesperado: {e}", "red")
        finally:
            self.after(0, self.scrape_button.configure, {"state": "normal", "text": "Iniciar Scrapeo"})

    # --- Funciones de Ayuda y Exportación ---
    
    def actualizar_gui_con_exito(self, texto_resultados, cantidad):
        """Actualiza la GUI y habilita botones de exportar."""
        self.actualizar_resultados(texto_resultados)
        self.actualizar_estado(f"Éxito: Se encontraron {cantidad} resultados.", "green")
        self.habilitar_botones_exportar(True)

    def habilitar_botones_exportar(self, habilitar):
        """Habilita o deshabilita los botones de exportación."""
        estado = "normal" if habilitar else "disabled"
        self.export_csv_button.configure(state=estado)
        self.export_excel_button.configure(state=estado)

    def exportar_a_csv(self):
        """Guarda los resultados en un archivo .csv"""
        if not self.lista_resultados:
            self.actualizar_estado("Error: No hay datos para exportar.", "red")
            return
        
        try:
            # Pedir al usuario dónde guardar el archivo
            filepath = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            )
            
            # Si el usuario cancela, filepath estará vacío
            if not filepath:
                return

            # Escribir los datos al archivo CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Indice", "Resultado"])  # Escribir la cabecera
                writer.writerows(self.lista_resultados)  # Escribir todos los datos
            
            self.actualizar_estado(f"Exportado a CSV con éxito.", "green")

        except Exception as e:
            self.actualizar_estado(f"Error al exportar CSV: {e}", "red")
# Mamá, mamá! mi papa esta tirando las cosas que no son suyas por la ventanaaaaaaaaaa..!

    def exportar_a_excel(self):
        """Guarda los resultados en un archivo .xlsx"""
        if not self.lista_resultados:
            self.actualizar_estado("Error: No hay datos para exportar.", "red")
            return

        try:
            # Pedir al usuario dónde guardar el archivo
            filepath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
            )

            if not filepath:
                return

            # Crear un nuevo libro de Excel y una hoja
            wb = Workbook()
            ws = wb.active
            ws.title = "Resultados Scrapeo"
            
            # Escribir la cabecera
            ws.append(["Indice", "Resultado"])
            
            # Escribir los datos
            for fila in self.lista_resultados:
                ws.append(fila)
            
            # Guardar el archivo
            wb.save(filepath)
            
            self.actualizar_estado(f"Exportado a Excel con éxito.", "green")
            
        except Exception as e:
            self.actualizar_estado(f"Error al exportar Excel: {e}", "red")

    # --- Funciones de Ayuda ---
    
    def actualizar_estado(self, mensaje, color):
        self.status_label.configure(text=f"Estado: {mensaje}", text_color=color)

    def actualizar_resultados(self, texto):
        self.results_textbox.configure(state="normal")
        self.results_textbox.delete("1.0", "end")
        self.results_textbox.insert("1.0", texto)
        self.results_textbox.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()