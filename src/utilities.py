import mysql.connector
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.opera.options import Options
from fake_useragent import UserAgent
import mysql.connector
import time
import random
from unicodedata import normalize
import unicodedata
import re
import json
import os
from pathlib import Path
import pyautogui

def conectar_bd ():
    # Carga parametros de configuracion
    params = load_config()
    config = {
        'user': params['database']['user'],
        'password': params['database']['password'],
        'host': params['database']['host'],
        'database': params['database']['database'],
    }

    try:
        cnx = mysql.connector.connect(**config)
        print("Conexión establecida- ")
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        exit()
    return cnx


def cerrar_bd(cnx):
    try:
        cnx.close()
        print("Conexión cerrada")
    except mysql.connector.Error as err:
        print(f"Error al cerrar la conexión: {err}")

def confg_navegador (PATH):
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    driver = webdriver.Opera(executable_path=PATH, options=options)

    # Obtener la resolución de la pantalla
    screen_width = driver.execute_script("return screen.width;")
    screen_height = driver.execute_script("return screen.height;")

    # Calcular la posición y el tamaño
    x_position = 500  
    y_position = 0  
    width = screen_width // 2 
    height = screen_height 

    # Posicion de la ventana
    driver.set_window_position(x_position, y_position)
    # Tamaño de la ventana
    driver.set_window_size(width, height)
    
    print ("Driver inicializado")
    return driver


# Inicializar Navegador y UserAgent
def inicializar(driver, NO_PAGINAS):

    # Genera User Agent
    user_agent = UserAgent()
    user_agents = [user_agent.random for _ in range(NO_PAGINAS)]
    print(f"User agent creados:{len(user_agents)}")

    # Inicializar navegador
    time.sleep(random.uniform(2, 4))
    driver.get('https://pagina.com')
    time.sleep(random.uniform(2, 4))


    # Acepta cookies
    try:
        boton_cookies = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[9]/div/div[2]/a')))
        boton_cookies.click()
    except:
        print ("No hay boton")
    return user_agents




def normalizar_cadena(titulo):
    if titulo is None:
        return ''
    # Convertir a minúsculas
    titulo = titulo.lower()
    # Eliminar acentos
    titulo = ''.join(c for c in unicodedata.normalize('NFKD', titulo) if unicodedata.category(c) != 'Mn')
    # Eliminar caracteres no alfanuméricos y espacios en blanco
    titulo = re.sub(r'[^a-zA-Z0-9]', '', titulo)
    return titulo


# Mapea numero (Funcion original modificada por privacidad)
def mapear_numero(numero):
    numero = float(numero)
    return numero

# Carga archivo config
def load_config():

    # Obtener la ruta del archivo actual
    current_dir = Path(__file__).resolve().parent
    config_path = (current_dir / '..' / 'config' / 'config.json').resolve()
    # Cargar el archivo JSON
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: El archivo de configuración no se encontró en {config_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error: El archivo de configuración no tiene un formato JSON válido")
        raise


