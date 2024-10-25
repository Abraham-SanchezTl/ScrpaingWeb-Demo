# Nombre del Proyecto
ScrapingWeb-Demo

## IMPORTANTE
Por motivos de confidencialidad, los nombres de las variables, los detalles específicos del código, y los archivos han sido modificados para proteger la información sensible. En esta demostración, solo se presenta el archivo explore_data.py, junto con su interacción con las utilidades y la interfaz gráfica. Aunque en la interfaz se muestra la ejecución de otros archivos, estos no están disponibles en esta versión, siendo únicamente para fines ilustrativos.

## Descripción
Este proyecto es una aplicación que combina scraping web y edición de archivos XLSX. Su objetivo es explorar una página web, establecer parámetros como el número de página, recorrer el contenido y extraer información. Además, incluye funcionalidades que permiten seleccionar y actualizar datos según criterios específicos, así como extraer información adicional no capturada inicialmente.

Una de las principales funciones es la actualización de publicaciones, que edita archivos XLSX previamente extraídos, encontrando las columnas correspondientes y asignando automáticamente los datos donde corresponda. También se incluye una opción para deshacer los cambios realizados, en caso de errores derivados de sistemas externos que interactúan con los archivos modificados.

La aplicación también permite la actualización de datos ya registrados en archivos, añadiendo criterios específicos propios del usuario. Todos los datos extraídos y actualizados se almacenan en una base de datos.

Cuenta con una interfaz gráfica que muestra el progreso de la ejecución en consola. Cabe destacar que esta aplicación tiene fines educativos y sirve para desarrollar habilidades en scraping y manipulación de datos.

## Estructura ORIGINAL del Proyecto
```bash
.
├── config
│   └── config.json
├── data
├── driver
│   ├── Importante
│   ├── operadriver
│   └── sha512_sum
├── gui
│   ├── config_explore_data.py
│   ├── config_update_data.py
│   ├── config_update_xlsx.py
│   ├── config_upload_xlsx.py
│   └── interface.py
├── LICENSE
├── main.py
├── README.md
└── src
    ├── __init__.py
    ├── explore_data.py
    ├── update_data.py
    ├── update_xlsx.py
    ├── upload_xlsx.py
    └── utilities.py
```

## Características
- Interfaz gráfica de usuario (GUI) intuitiva.
- Procesos ETL (Extract, Transform, Load)
- Scraping.
- Manejo de User Agents.
- Almacenamiento en base de datos.
- Edición automática de archivos XLSX
- Parámetros configurables
- Ejecución en consola

## Requisitos
- Python 3.10.9
- Librerías especificadas en `requirements.txt`.


### Ejemplos de Uso
- Scraping de datos desde una página web
El programa permite extraer información de una página web especificando un rango de páginas para explorar. Una vez configurados los parámetros en la interfaz gráfica (como el número de páginas a recorrer), la aplicación utiliza Selenium para realizar el scraping, almacena los datos en una base de datos y permite aplicar criterios de selección a los resultados obtenidos.

Ejemplo:

Establecer el rango de páginas separados por coma (6, 7, 9).
Al guardar la configuración empieza la extracción.

- Scraping para actualización de datos desde una página web
Establecer parámetros para actualización según criterios.
Establecer rango de fecha.
Al guardar la configuración inicia la extracción y actualización.

Ejemplo:

Seleccionar parametros de seleccion.
Establecer rango de fechas.
Extrae nuevos datos encontrados

- Edición automática de archivos XLSX
El programa puede tomar los datos procesados y editarlos automáticamente en un archivo XLSX, asignando la información a las columnas correctas. Esto se hace fila por fila y permite actualizar los registros ya existentes en el archivo.

Ejemplo:

Seleccionar un archivo XLSX previamente generado.
Editar el archivo asignando los nuevos datos extraídos a las columnas correspondientes.
Deshacer los cambios si es necesario, en caso de errores.

### Contacto
Para cualquier pregunta o sugerencia, puedes contactarme en:

Email: abraham.tlatelpa00@gmail.com
