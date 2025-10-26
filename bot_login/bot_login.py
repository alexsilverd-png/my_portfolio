import time
from playwright.sync_api import sync_playwright, Playwright

def run(playwright: Playwright):
    # ¿Por qué los programadores prefieren el modo oscuro?
    # Porque la luz atrae a los bugs xD xd dxXDdd

    # Configuración de debug: ver UI, acciones lentas.
    browser = playwright.chromium.launch(headless=False, slow_mo=500)
    page = browser.new_page()

    # 1. IR AL SITIO
    print("Navegando a http://quotes.toscrape.com/login ...")
    page.goto("http://quotes.toscrape.com/login")

    # 2. LLENAR DATOS (admin/admin)
    print("Rellenando formulario...")
    page.get_by_label("Username").fill("admin")
    page.get_by_label("Password").fill("admin")

    # 3. CLIC EN LOGIN
    print("Haciendo clic en 'Login'...")
    page.get_by_role("button", name="Login").click()

    # 4. VERIFICAR LOGIN
    # Esperar el 'Logout' es la aserción principal.
    print("Verificando inicio de sesión...")
    page.wait_for_selector("text=Logout")
    
    print("¡Inicio de sesión exitoso!")

    # (Extra) Scrapear un dato para confirmar.
    primera_cita = page.locator("div.quote > span.text").first.inner_text()
    print(f"\n[DATO EXTRAÍDO] Primera cita en la página: {primera_cita}")

    # Pausa para inspección visual. Quitar en prod.
    print("\nCerrando el navegador en 5 segundos...")
    time.sleep(5)
    
    # 5. LIMPIAR
    browser.close()

# 'with' gestiona el ciclo de vida del proceso de Playwright.
with sync_playwright() as playwright:
    run(playwright)