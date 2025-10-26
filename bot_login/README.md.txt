=========================
Bot de Login (Playwright)
=========================

Un bot simple para automatizar el inicio de sesión en un sitio web
de demostración usando Playwright.

---
Características
---
* Automatiza el inicio de sesión en un sitio web de prueba.
* Rellena automáticamente las credenciales (admin/admin).
* Verifica que el inicio de sesión sea exitoso.
* Extrae un dato de la página post-login para confirmar.
* Configurado para verse en tiempo real (modo no-headless).

---
Requisitos
---
* Python 3.7+
* playwright (biblioteca de Python)

---
Instalación
---
Puedes instalar la dependencia y los navegadores necesarios.
Abre tu terminal y ejecuta:

1. Instalar la biblioteca:
   pip install playwright

2. Instalar los navegadores (solo se hace una vez):
   playwright install

---
Modo de Uso
---
1. Ejecuta el script de Python:
   python bot_login.py

2. El script se ejecutará automáticamente.

3. Verás cómo se abre un navegador, se rellena el formulario
   y se inicia sesión.

4. Los resultados (y el dato extraído) se mostrarán en la terminal.

5. El navegador se cerrará solo después de 5 segundos.

---
Sitio de Prueba Utilizado
---
Este script está configurado para usarse en el siguiente sitio,
que está diseñado para practicar automatización:

* URL del Sitio: http://quotes.toscrape.com/login
* Credenciales:
  - Username: admin
  - Password: admin

---
¡IMPORTANTE! - Modo de Depuración
---
Este script está configurado para *depuración y demostración*.
Por eso puedes ver el navegador (headless=False) y las acciones
son lentas (slow_mo=500).

Para un uso en un servidor (producción), debes cambiar la
configuración de lanzamiento a "headless=True" y "slow_mo=0",
y quitar el "time.sleep(5)" del final del script.