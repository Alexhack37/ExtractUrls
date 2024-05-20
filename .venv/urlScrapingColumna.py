from bs4 import BeautifulSoup
import pandas as pd
import requests


def scrape_images(site):
    r = requests.get(site)
    s = BeautifulSoup(r.text, "html.parser")

    image_urls = set()

    for img_tag in s.find_all("img"):
        src = img_tag.attrs.get('src')
        if src and src.startswith(('http://', 'https://')):
            image_urls.add(src)

    for meta_tag in s.find_all("meta", property="og:image"):
        content = meta_tag.attrs.get('content')
        if content and content.startswith(('http://', 'https://')):
            image_urls.add(content)
    return list(image_urls)
    #for img_url in image_urls:

    #   print(img_url)

    #df = pd.DataFrame(image_urls)

if __name__ == "__main__":
    #filasALeer = int(input('Cuantas filas a leer:'))
    enlacesExcel = pd.read_excel('./enlacesLeer.xlsx',usecols=[0], sheet_name="Páginas", nrows=2-1)
    #print(enlacesExcel)

    lista_enlaces = enlacesExcel.iloc[:, 0].tolist()
    df_final = pd.DataFrame()

    # Recorrer la lista con un bucle for
    for i, enlace in enumerate(lista_enlaces):
        # Haz lo que necesites con cada enlace
        site= enlace
        enlaces = scrape_images(site)
        #df = pd.DataFrame({f'Enlaces_Pagina_{i + 1}': enlaces})
        df = pd.DataFrame({enlace : enlaces})

        # Añadimos los enlaces de la página actual al DataFrame final
        df_final = pd.concat([df_final, df], axis=1)
        print(i)
    # Escribimos el DataFrame final en un nuevo archivo Excel
    df_final.to_excel('./enlaces.xlsx', index=False)

