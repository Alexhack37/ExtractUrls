import requests
from bs4 import BeautifulSoup
import pandas as pd

# Inicializa una lista para almacenar las URLs
g = []
for i in range(50):
    dir = input()
    g.append(dir)

# Inicializa una lista para almacenar los datos de las empresas
empresas = []

def webindiv(url):
    empresasDatos = {
        "Nombre": None,
        "direccion": None,
        "telefono": None,
        "web": None
    }

    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}
    r = requests.get(url=url, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')

    # Extrae el nombre
    contenedorTitulo = soup.find('div', class_='itemh p1 pb2')
    if contenedorTitulo:
        titulo = contenedorTitulo.find('h1')
        if titulo:
            empresasDatos['Nombre'] = titulo.text.strip()

    # Extrae la dirección
    globalDiv = soup.find('div', class_='flex flex-wrap clearfix')
    if globalDiv:
        direccionDiv = globalDiv.find('div', class_='mb1 map')
        if direccionDiv:
            direccion = direccionDiv.find('div', class_='mb1')
            if direccion:
                empresasDatos['direccion'] = direccion.get_text(strip=True)

    # Extrae el teléfono
    telefo = soup.find('div', class_='col-9 lg-col-10 pl1 lnk')
    if telefo is None:
        telefo = soup.find('div', class_='col-9 pl1 lnk')
    if telefo:
        tel = telefo.find_all('span')
        if len(tel) > 1:
            empresasDatos['telefono'] = tel[1].get_text(strip=True)

    # Extrae el enlace web
    col9 = soup.find_all('div', class_='col-9 lg-col-10 pl1 lnk')
    if not col9:
        col9 = soup.find_all('div', class_='col-9 pl1 lnk')
    if col9:
        for div in col9:
            aas = div.find('a')
            if aas:
                link = aas.get('href')
                if link:
                    empresasDatos['web'] = link
                    break

    empresas.append(empresasDatos)

# Recorre las URLs y procesa cada una
for i in g:
    url = "https://www.ineventos.es" + i
    print(i)
    webindiv(url)

df = pd.DataFrame(empresas)
df.to_excel("empresas_24Mejores.xlsx", index=False)



"""
/acheazafatas
/andromedaeventos
/optimizaeventos
/salagotouch
/domo360
/celebrandoencasa
/alehopeventos
/endlessdreams
/layouteventsmadrid
/eltallerdeprotocolo
/chupetesicorbatas
/despedidaspeoplemadrid
/eventosmagicosmadrid
/4foreverything
/party10
/unityeventos
/click2events
/centralfiestas
/myomyoeventos
/crombyscomunicacion
/medialed
/micropolix
/rubertproducciones
/eventosyshows
/milagbodasdeensueno
/carpa10carpasyserviciosasociados
/eteria
/audiovisualline
/sunset80s
/grupokodru
/cocteleriaelmojito
/goblincatering
/familymoon
/dimar
/customvote
/kidseventosyocio
/super8
/enbuenasmanosbodas
/casapatasflamencoenvivo
/localelmundomagico
/dimequemequieres
/speakerstar
/latararadisenoefimero
/fabricandosuenos
/curcumacateringyeventos
/calandria
/horalocamadrid
/atipica
/rayfertv
/escuelainfantilcottons
/cateringleyve
/dagor
/anakaterina
/maestroceremoniasmadrid
/positivarte
/eventosaloloko

"""