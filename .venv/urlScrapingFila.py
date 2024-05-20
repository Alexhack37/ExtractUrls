from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape_images(site):
    r = requests.get(site)
    s = BeautifulSoup(r.text, "html.parser")

    image_urls = set()

    for img_tag in s.find_all("img"):
        src = img_tag.attrs.get('src')
        if src and src.startswith(('http://', 'https://')) and 'facebook' not in src and 'ASTERISCO.webp' not in src and 'logo' not in src and 'lg1' not in src:
            image_urls.add(src)

    for meta_tag in s.find_all("meta", property="og:image"):
        content = meta_tag.attrs.get('content')
        if content and content.startswith(('http://', 'https://')) and 'facebook' not in content and 'ASTERISCO.webp' not in content and 'logo' not in content and 'lg1' not in content:
            image_urls.add(content)
    return list(image_urls)



if __name__ == "__main__":
    enlacesExcel = pd.read_excel('./enlacesLeer.xlsx', usecols=[0], sheet_name="Páginas", nrows=500)
    lista_enlaces = enlacesExcel.iloc[:, 0].tolist()

    # Creamos un DataFrame vacío
    df_final = pd.DataFrame()

    for i, enlace in enumerate(lista_enlaces):
        site = enlace
        enlaces = scrape_images(site)

        # Creamos un DataFrame temporal para los enlaces de esta página
        df_temp = pd.DataFrame({'Enlaces': enlaces})

        # Añadimos una columna para identificar de qué página son los enlaces
        df_temp['Página'] = enlace
        print(i)
        # Concatenamos este DataFrame temporal al DataFrame final
        df_final = pd.concat([df_final, df_temp])

    # Escribimos el DataFrame final en un nuevo archivo Excel
    df_final.to_excel('./enlacesFila.xlsx', index=False)
