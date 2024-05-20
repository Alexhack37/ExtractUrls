import os
import shutil
import pandas as pd


#given a excel with links, read them, get the name of the file at the end, conserve the file extension
#and its file directory usualy a date, go to os, select it, copy and paste in a selected location
#ab
def find(prefix, name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            ruta = os.path.relpath(root,path)
            if not os.path.exists('C:\\cosasAlex\\web y cosas\\FTP_images_Nuevo\\'+ ruta):
                os.makedirs('C:\\cosasAlex\\web y cosas\\FTP_images_Nuevo\\'+ ruta)
            #if prefix in files:
            if name == prefix:
                shutil.copyfile(os.path.join(root, name),
                                'C:\\cosasAlex\\web y cosas\\FTP_images_Nuevo\\' + ruta + "\\" + name)
            else:
                shutil.copyfile(os.path.join(root, name),
                            'C:\\cosasAlex\\web y cosas\\FTP_images_Nuevo\\' + ruta + "\\" + prefix)
                shutil.copyfile(os.path.join(root, name),
                                'C:\\cosasAlex\\web y cosas\\FTP_images_Nuevo\\' + ruta + "\\" + name)





if __name__ == "__main__":

    enlacesExcel = pd.read_excel('./enlacesArchivosGoogle.xlsx', usecols=[0], sheet_name="Img", nrows=884)
    lista_enlaces = enlacesExcel.iloc[:, 0].tolist()
    for i, enlace in enumerate(lista_enlaces):
        print(i)
        if isinstance(enlace, tuple):
            enlace = enlace[0]
        partes = enlace.split('/')
        archivo = partes[-1]


        base_name = os.path.splitext(archivo)[0]
        extension = os.path.splitext(archivo)[1]

        # Determinar el prefijo adecuado
        index_of_x = base_name.find('x')
        if index_of_x != -1:
            # Buscar el primer guion antes de la 'x'
            index_of_dash = base_name.rfind('-', 0, index_of_x)
            if index_of_dash != -1:
                prefijo = base_name[:index_of_dash] + extension
        else:
            prefijo = base_name + extension
        #print(prefijo)
        find(prefijo, archivo, 'C:\\cosasAlex\\web y cosas\\FTP_images\\')