import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import load_workbook
import re


def obtener_datos_empresa(datos):
    """Convierte una lista de datos en un diccionario con campos específicos"""
    empresa = {
        "direccion": "",
        "telefono": None,
        "email": None,
        "web": None
    }

    for dato in datos:
        if "@" in dato:
            empresa["email"] = dato
        elif "http" in dato or dato.startswith("www"):
            empresa["web"] = dato
        elif any(char.isdigit() for char in dato) and (len(dato) >= 9 and len(dato) <= 15): # Assuming phone number length
            empresa["telefono"] = dato
        else:
            if empresa["direccion"]:
                empresa["direccion"] += ", " + dato
            else:
                empresa["direccion"] = dato

    return empresa

if __name__ == "__main__":
    URL = "https://madridfilmoffice.com/business_category/productoras-de-eventos-y-espectaculos/"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0"}

    r = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')

    nombres = soup.findAll('h4', {"class": "name"})
    datos1 = soup.findAll('div', {"class": "col1"})
    datos2 = soup.findAll('div', {"class": "col2"})
    descripciones = soup.findAll('div', {"class": "colall"})

    empresas = []

    for nombre, dato1, dato2, descripcion in zip(nombres, datos1, datos2, descripciones):
        nombre_text = nombre.get_text(strip=True)
        datos1_text = dato1.get_text(separator="|", strip=True).split("|")
        datos2_text = dato2.get_text(separator="|", strip=True).split("|")
        datosTotal = datos1_text + datos2_text

        if 'Contacto' in datosTotal:
            datosTotal.remove('Contacto')
        if 'Tel:' in datosTotal:
            datosTotal.remove('Tel:')
        if datosTotal[0] == '':
            datosTotal.pop(0)

        empresa_datos = obtener_datos_empresa(datosTotal)
        empresa_datos["nombre"] = nombre_text
        empresa_datos["descripcion"] = descripcion.get_text(strip=True)
        empresas.append(empresa_datos)
        print(empresa_datos, end="\n")
    print(empresas)

    df = pd.DataFrame(empresas)
    df.to_excel("empresas_eventos.xlsx", index=False)