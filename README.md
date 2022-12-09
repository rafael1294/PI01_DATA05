#            PROYECTO INDIVIDUAL #1 : DATA ENGINEER 


# Descripción del proyecto:

Construir una "API" para poder hacer consultas sobre las plataformas: 
- Amazon
- Disney 
- Hulu  
- Netflix<br><br>

# Proceso ETL:

- 1: El proceso ETL se ejecuta en el archivo "PI-01.ipynb". <br>

- 2: Los archivos "csv." en la carpeta "Datasets" son leidos y ejecutados por este archivo, luego son transformados y finalmente se genera archivos "csv." dentro de la carpeta "tables".<br><br>

# MySql:

- Importamos las tablas a MySql y realizamos las querys para su comprobación. <br><br>

# PyMySql:

- Realizamos la conexión con la base de datos "PI" desde python y generamos las consultas para su ejecución en la API.<br><br> 

# API:

- El archivo "main.py" dentro de la carpeta "app" contiene todas las funciones que la aplicación necesita para realizar sus consultas a la base de datos.<br><br>

# Parámetros de la API:

- get_max_duration: <br>
    Parametros: Año, plataforma y tipo de tiempo("min" o "season")<br>
    Resultado: Pelicula o serie con mayor duración y cuanto es esta duración.<br>

- get_count_plataform: <br>
        Parametros: Plataforma.<br>
        Resultado: Cantidad de películas y series de la plataforma seleccionada.<br>

- get_listedin: <br>
    Parámetros: Género de película o serie.<br>
    Resultado: Plataforma con más contenido del género seleccionado y su cantidad.<br>

- get_actor: <br>
    Parámetros: actor/actriz<br>
    Resultado: Plataforma en la que más se encuentra el actor/actriz escogido y su cantidad.<br><br>

