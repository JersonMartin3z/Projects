from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def scrape_crypto_data():
    # Columnas
    fields = ["symbol", "name", "price", "change", "change_%",
              "market_cap", "vol_total", "vol_last_24", "vol_t_last_24",
              "vol_circ"]

    # Inicializar el navegador
    driver = webdriver.Chrome()

    # URL de la página inicial
    url = "https://es.finance.yahoo.com/criptomonedas/"
    driver.get(url)

    # Esperar a que el pop-up aparezca y aceptarlo
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Aceptar")]'))
        )
        accept_button.click()
    except Exception as e:
        print(f"No se encontró el botón de aceptar: {e}")

    # Lista para almacenar los datos de todas las páginas
    all_data = []

    # Función para extraer datos de la tabla de la página actual
    def extract_table_data():
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table')
        
        if table: 
            rows = table.find('tbody').find_all('tr')
            
            data = []
            for row in rows:
                cols = row.find_all('td')
                cols = [col.text.strip() for col in cols[:10]]
                if cols:
                    data.append(cols)
            
            return data
        
        return None

    # Extraer datos de la primera página
    data = extract_table_data()
    if data:
        all_data.extend(data)

    # Iterar sobre las páginas siguientes
    while True:
        try:
            # Verificar si el botón "siguiente" está habilitado
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[title="Siguiente página"]'))
            )

            # Verificar si el botón "siguiente" está deshabilitado
            if next_button.get_attribute('aria-disabled') == 'true':
                print("Botón de siguiente página deshabilitado, fin de paginación.")
                break

            # Clic en el botón de siguiente página
            next_button.click()
            
            # Esperar hasta que la nueva tabla se cargue
            WebDriverWait(driver, 10).until(
                EC.staleness_of(next_button)
            )

            # Extraer datos de la nueva página
            data = extract_table_data()
            if data:
                all_data.extend(data)
        except Exception as e:
            print(f"No se pudo acceder a la siguiente página: {e}")
            break

    # Crear el DataFrame final con todos los datos extraídos
    if all_data:
        cryptos = pd.DataFrame(all_data, columns=fields)
    else:
        cryptos = pd.DataFrame(columns=fields)
        print("No se encontraron datos.")

    # Cerrar el navegador
    driver.quit()

    return cryptos

