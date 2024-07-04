from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd


def dataTracker(URL, empresas):
    empresasDatos = {
        "Nombre": None,
        "direccion": None,
        "telefono": None,
        "email": None,
        "web": None
    }

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}

    r = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    content_section = soup.find('div', class_='content-section')
    if content_section:
        paragraphs = content_section.find_all('p')

        names = soup.find('div', class_='col-12 col-lg-7')
        if names:
            h1_name = names.find('h1')
            if h1_name:
                empresasDatos['Nombre'] = h1_name.text.strip()

        if len(paragraphs) > 1:
            empresasDatos['direccion'] = paragraphs[1].get_text(strip=True)

        try:
            links = soup.find('div', class_='links')
            if links:
                enlaces = links.find_all('a')
                if len(enlaces) > 2:
                    empresasDatos['telefono'] = enlaces[1].get('data-text', 'N/A')
                    empresasDatos['email'] = enlaces[2].get('data-text', 'N/A')
                    if len(paragraphs) > 2:
                        empresasDatos['web'] = paragraphs[2].get_text(strip=True)
            empresas.append(empresasDatos)
        except:
            print("no data")
    return empresas


if __name__ == "__main__":
    # Configurar Selenium con Edge
    empresas = []
    options = Options()
    options.use_chromium = True  # Necesario para usar Edge basado en Chromium
    options.headless = True  # Ejecutar en modo headless, sin ventana gráfica

    # Reemplaza con la ruta a tu msedgedriver
    edge_service = EdgeService(executable_path='C:/cosasAlex/web y cosas/msgdrivershit/msedgedriver.exe')

    # Crear instancia del navegador
    driver = webdriver.Edge(service=edge_service, options=options)
    #driver.get("https://www.eventoplus.com/agencias/agencias-de-eventos/madrid/")
    #driver.get("https://www.eventoplus.com/agencias/agencias-de-eventos-virtuales/")
    #driver.get("https://www.eventoplus.com/agencias/agencias-de-espectaculos-para-eventos/")
    #driver.get("https://www.eventoplus.com/agencias/agencias-de-incentivos/madrid/")
    #driver.get("https://www.eventoplus.com/agencias/empresas-de-organizacion-de-congresos-opc/madrid/")
    driver.get("https://www.eventoplus.com/agencias/agencias-de-marketing-promocional/madrid/")

    # Esperar a que la página se cargue completamente
    time.sleep(10)  # Ajusta este tiempo si es necesario

    # Hacer clic en "Cargar más" hasta que no haya más empresas
    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'filtro-more'))
            )
            load_more_button.click()
            time.sleep(10)  # Esperar a que se carguen más empresas
        except:
            break  # No hay más botones de "Cargar más"

    # Obtener el HTML después de que se haya cargado todo el contenido
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    driver.quit()

    # Encontrar los títulos
    div_elements = soup.find_all('div', class_='title')

    for div_element in div_elements:
        h3_element = div_element.find('h3')
        if h3_element:
            anchor_tag = h3_element.find('a')
            if anchor_tag:
                link = anchor_tag.get('href')
                empresas = dataTracker(link, empresas)

    df = pd.DataFrame(empresas)
    df.to_excel("empresas_eventos_NUEVO.xlsx", index=False)
