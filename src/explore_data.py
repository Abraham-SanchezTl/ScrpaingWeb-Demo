from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.opera.options import Options
from fake_useragent import UserAgent
import re
from datetime import datetime
import mysql.connector
import pandas as pd
import time
import random
import os
import shutil
import urllib
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import date
from .utilities import conectar_bd
from .utilities import inicializar
from .utilities import confg_navegador
from .utilities import cerrar_bd
from .utilities import load_config
import json
from pathlib import Path
from selenium.common.exceptions import NoSuchWindowException, WebDriverException


# Funcion para recorrer la pagina
# Recibe como parametro el url dividio en 2 partes, una lista de user agents creados anteriormente, un cursor, los indices que se quieren recorrer, y el driver inicializando
def recorrer_pagina(web_path_1, web_path_2, user_agents, cursor, indices_pagina, driver):
    contador = 0 
    for indice_pagina in indices_pagina:
        print("Tamaño de user_agents:", len(user_agents))
        print("Valor de indice_pagina:", indice_pagina)

        # Estblece UserAgent
        ua = user_agents[contador]
        options = Options()
        options.add_argument(f"--user-agent={ua}")

        print(f"User-Agent: {ua}")
        print(f"Numero de pagina: {indice_pagina}")
        driver.get(f"{web_path_1}{indice_pagina+1}{web_path_2}")
        print(f"Link actual: {web_path_1}{indice_pagina+1}{web_path_2}")
        time.sleep(2)
        contador += 1

        # Existen 72 secciones por pagina que recorreremos
        # 5 secciones por fila y por lo tanto se recorrera en grupos de 5
        indices = list(range(72))
        for i in range(0, 72, 5):

            # El recorrido se ejecuta en grupos de 5 aleatoriamente
            grupo = indices[i:i+5]
            random.shuffle(grupo)
            
            # Recorrer los elementos mezclado
            for elemento in grupo:
                scrap_elemento(elemento, cursor, driver) # Scrap elemento
                time.sleep(random.uniform(2, 4))




# Scraping del elemento

def scrap_elemento(i, cnx, driver):
    variable25 = None
    variable26 = None
    variable27 = None
    variable28 = None
    
    caracteres_a_eliminar = '●•·—-–»«√ōū<>®|'
    cursor = cnx.cursor()

    print("-------------------------------------------------")
    print(f"Elemento : {i+1}")
    time.sleep(random.uniform(2, 4))

    # Url del elemento
    pagina = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div/div[5]/div['+str(i+1)+']/div/div/div[2]/div[1]/p[2]/a')))
    url = pagina.get_attribute('href')

    # Imprime la URL
    print(f"url: {url}" )
    # Obtiene la fecha de hoy
    hoy = datetime.today().date()

    # Consulta si existe previamente
    consulta = ("SELECT EXISTS(SELECT 1 "
            "FROM historial_precios "
            "INNER JOIN tabla1 ON tabla2.producto_id = productos.id "
            "WHERE tabla1.variable10 = %s AND DATE(tabla2.variable11) = %s)")

    # Ejecuta la consulta
    cursor.execute(consulta, (url, hoy))
    variable12 = cursor.fetchone()

    # Verifica si ya esta en la base con fecha de hoy
    if variable12[0]:
        print("La URL ya está en la base de datos con la fecha de hoy.")
    else:
        print("La URL no está en la base de datos con la fecha de hoy.")
        pagina.click()
        time.sleep(random.uniform(2, 4))

        # Obtener id del producto
        id_product = driver.find_element_by_xpath('/html/body/div[1]/main/div/div[3]')
        id_ = id_product.get_attribute('id')
        print(f"ID: {id_}")


        variable13 = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="'+id_+'"]/div/div[1]/div/div[2]')))
        url_actual = driver.current_url

        print(url_actual)

        # Extraccion de datos
        variable14 = (variable13.text).split("\n")
        variable15 = variable14[0]
        print(f"variable15: {variable15}")

        # Establecemos una palabra de patron para extraer la informacion exacta que necesitamos
        patron = r'variable16: (.+?)\n'
        variable16 = re.search(patron, variable13.text)
        print("variable16:", variable16.group(1))#
        
        variable17 = re.search(r"variable17:\s*([a-zA-Z]+).*", variable13.text)
        if variable17:
            variable17_=variable17.group(1)
        else:
            variable17_="Sin categoria"
        print(f"Categoria: {variable17_}")

        patron = r'variable18:\s(\w+)\s\|\s'
        variable18 = re.search(patron, variable13.text)
        if variable18:
            print(f"variable18: {variable18.group(1)}")
        else:
            patron = r"variable18:\s*(\w+)AGOTADO"
            variable18 = re.search(patron, variable13.text)
            if variable18:
                print(f"variable18: {variable18.group(1)}")
            else:
                patron = r'variable18: (.+?)\n'
                variable18 = re.search(patron, variable13.text)
                print(f"variable18: {variable18.group(1)}")

        
        variable19 = datetime.now()
        variable20 = datetime.now().strftime('%Y-%m-%d')
        print(variable20)
        print(f"variable19 : {variable20}")

        patron = r'\$([\d,]+(?:\.\d+)?)'
        variable21 = re.search(patron, variable13.text)
        variable22 = variable21.group(1).replace(",", "")
        variable22 = variable22[: len(variable22)-2] + "." + variable22[len(variable22)-2: len(variable22)]
        variable22=float(variable22)
        print(f"variable22 : {variable22}")

        patron = r'variable_23: (.+?)\n'
        variable_23_m = re.search(patron, variable13.text)
        variable_23=variable_23_m.group(1).replace(",", "")
        variable_23=variable_23[1: len(variable_23)-2] + "." + variable_23[len(variable_23)-2: len(variable_23)]
        variable_23=float(variable_23)
        print(f"variable_23 : {variable_23}")


        
        elemento = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="'+id_+'"]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]')))
        driver.execute_script("arguments[0].scrollIntoView();", elemento)
        driver.execute_script("window.scrollBy(0, arguments[0].scrollHeight);", elemento)
        variable24 = elemento.text
        traduccion = str.maketrans("", "", caracteres_a_eliminar)
        variable24 = variable24.translate(traduccion)
        print(f"variable24 : {variable24}")
        

        #busca el elemento para buscar la seccion de informacion adicional
        elemento = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="'+id_+'"]/div[1]/div[2]/div/div[2]/div[2]/div/div[1]/h5')))
        informacion_adicional = elemento.text



        if informacion_adicional == 'INFORMACIÓN ADICIONAL':
            base_xpath = '//*[@id="'+id_+'"]//div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[{}]/th'
            base_xpath2 = '//*[@id="'+id_+'"]//div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div/table/tbody/tr[{}]/td'
            num_elements = len(driver.find_elements_by_xpath(base_xpath.format('*')))
            for i in range(1, num_elements + 1):
                xpath = base_xpath.format(i)
                xpath2 = base_xpath2.format(i)
                # Construir el xpath específico para el índice 
                element = driver.find_element_by_xpath(xpath)
                element2 = driver.find_element_by_xpath(xpath2)
                # Realizar acciones con el elemento, por ejemplo, imprimir el texto
                if element.text == 'variable25':
                    variable25 = element2.text
                    print(element2.text)
                elif element.text == 'variable26':
                    variable26 = element2.text
                    print(variable26)
                elif element.text == 'variable27':
                    variable27 = element2.text
                    print(variable27)
                elif element.text == 'GÉNERO':
                    variable28 = element2.text
                    print(variable28)



        else:
            print("entra else")
            elemento = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="'+id_+'"]/div[1]/div[2]/div/div[2]/div[3]/div/div[1]/h5')))
            informacion_adicional = elemento.text
            if informacion_adicional == 'INFORMACIÓN ADICIONAL':
                base_xpath = '//*[@id="'+id_+'"]//div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div/table/tbody/tr[{}]/th'
                base_xpath2 = '//*[@id="'+id_+'"]//div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div/table/tbody/tr[{}]/td'
                num_elements = len(driver.find_elements_by_xpath(base_xpath.format('*')))
                for i in range(1, num_elements + 1):
                    xpath = base_xpath.format(i)
                    xpath2 = base_xpath2.format(i)
                    # Construir el xpath específico para el índice 
                    element = driver.find_element_by_xpath(xpath)
                    element2 = driver.find_element_by_xpath(xpath2)
                    # Realizar acciones con el elemento, por ejemplo, imprimir el texto
                    if element.text == 'variable25':
                        variable25 = element2.text
                        print(element2.text)
                    elif element.text == 'variable26':
                        variable26 = element2.text
                        print(variable26)
                    elif element.text == 'variable27':
                        variable27 = element2.text
                        print(variable27)
                    elif element.text == 'variable28':
                        variable28 = element2.text
                        print(variable28)


        driver.execute_script("window.scrollTo(0, 0);")


        # Guarda la informacion estructurada en la base de datos
        if variable25 is not None and variable26 is not None and variable27 is not None and variable28 is not None :
            # Verificar si el producto  ya existe en la tabla
            consulta = f"SELECT COUNT(*) FROM tabla1 WHERE variable16 = '{ variable16.group(1)}'"
            cursor.execute(consulta)
            resultado = cursor.fetchone()[0]
            # Si el resultado no existe, procede a guardar el elemento
            if resultado == 0 :
                print("Aun no registrado ... procediendo a registrar")
                query = "INSERT INTO tabla1 (variable15, variable18, variable16, variable17_, url, variable24, variable25, variable27, variable28, variable26) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (variable15, variable18.group(1), variable16.group(1), variable17_, url_actual, variable24, variable25, variable27, variable28, variable26)
                cursor = cnx.cursor()
                cursor.execute(query, values)
            else:
                print ("Ya registrado")
            cnx.commit()


            query = "SELECT id FROM tabla1 WHERE variable16 = %s"# nombre es tienda_texto
            cursor.execute(query, ( variable16.group(1),))
            id_producto = cursor.fetchone()[0]
            fuencion_scrap_adicional(id_producto, variable20, variable_23, variable22, cursor, driver, cnx)

            time.sleep(random.uniform(2, 4))
        
        driver.back()


# Realiza scraping en otra seccion dentro de la pagina
def fuencion_scrap_adicional (id_producto, variable20, variable_23, variable22, cursor, driver, cnx) :
    # Encuentra sección
    try:
        variable29 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="disp_prod"]')))
        variable29.click()
        time.sleep(random.uniform(1, 3))
        path_inicio = '//*[@id="status_disponibilidad_tienda"]/ul/li['
        path_fin_tienda = ']/div[1]/div[1]/div/h3'
        path_fin_variable30 = ']/div[1]/div[2]/div/div/h3'
        for i in range(120):
            variable31 = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, path_inicio+str(i+1)+path_fin_tienda)))
            variable30 = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, path_inicio+str(i+1)+path_fin_variable30)))
            variable31_texto = variable31.text
            variable30_texto = variable30.text
            variable32 = int(variable30_texto)
            print(variable31_texto, ":", variable32)
            # Verifica existencia
            if variable32 > 0:
                query = "SELECT id FROM tabla3 WHERE nombre = %s"  
                cursor.execute(query, (variable31_texto,))
                result = cursor.fetchone()

                if result is None:
                    # Código para manejar el caso cuando no se encuentra la tienda
                    print("No existe")
                    sql = "INSERT INTO tabla3 (nombre) VALUES (%s)"
                    cursor.execute(sql, (variable31_texto,))
                    print("No existente en la Base de datos...", variable31_texto, "Agregada correctamente")
                    cursor.execute(query, (variable31_texto,))
                    result = cursor.fetchone()

                id_tienda = result[0]
                consulta = "INSERT INTO historial_precios (tienda_id, producto_id, fecha_hora, precio_tienda, precio_online, existencia) VALUES (%s, %s, %s, %s, %s, %s)"
                valores = (id_tienda, id_producto, variable20, variable_23, variable22, variable32)
                cursor.execute(consulta, valores)   

        cnx.commit()

    except TimeoutException:
        print("No hay disponibilidad de producto:")
        return
    

def main():

    print("Iiniciando explloracion")
    config = load_config()


    # Ingresar indices a recorrer
    indices_pagina = config['explore_settings']['pages']
    NO_PAGINAS = len(indices_pagina)

    # Obtener ruta del driver
    current_dir = Path(__file__).resolve().parent
    PATH = (current_dir / '..' / 'driver' / 'operadriver').resolve()


    URL_1='https://pagina.com/catalogo/page/'
    URL_2='/?buscar_productos=1&pa_plataforma=nsw%2Cps3%2Cps4%2Cps5%2Cxbx%2Cxsx%2Cxss%2Cwiiu%2Cxone%2Cwii'
    # Conecta a base de datos y devuelve cnx
    cnx = conectar_bd()
    # Configura navegador
    driver = confg_navegador(PATH)
    # Abre home, crea UserAgent y acepta cookies
    try:
        user_agents = inicializar(driver, NO_PAGINAS)
        recorrer_pagina(URL_1, URL_2, user_agents, cnx, indices_pagina, driver)
    except (NoSuchWindowException, WebDriverException):
        driver.quit()
    
    driver.quit()
    cerrar_bd(cnx)
    print("Exploracion terminada terminada.")


if __name__ == "__main__":
    main()











