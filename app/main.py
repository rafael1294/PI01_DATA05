from fastapi import FastAPI
from starlette.responses import RedirectResponse
import pymysql

app = FastAPI()


def conectar_a_base_de_datos() :
    conexion = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'mysql123M',
    db= 'pi',
    port= 3306
    )
    return conexion.cursor()


#1 Funcion que recibe año y plataforma y tipo de tiempo y retorna la pelicula o serie y su duracion maxima.
def max(anio,plataforma,time):
    cursor=conectar_a_base_de_datos()
    a=[]
    p=0
    anio=str(anio)
    if plataforma == "amazon":
        p = 1
    elif plataforma == "disney":
        p = 2
    elif plataforma == "hulu":
        p = 3
    elif plataforma == "netflix":
        p = 4
    else:
        "Inserte: amazon, disney, hulu o netflix"
    p=str(p)  
    if time=="min":
        query="select Id_Plataform, title, release_year, convert(SUBSTRING_INDEX(duration,' ', 1), UNSIGNED INTEGER)  AS tiempo, \
        SUBSTRING_INDEX(duration,' ', -1) as Unidades \
        from dffilm \
        where release_year = "+anio+" and Id_Plataform = '"+p+"' and SUBSTRING_INDEX(duration,' ', -1) like 'min%' \
        order by 4 desc \
        limit 1"
        cursor.execute(query)
    elif time=="season":
        query="select Id_Plataform, title, release_year, convert(SUBSTRING_INDEX(duration,' ', 1), UNSIGNED INTEGER)  AS tiempo, \
        SUBSTRING_INDEX(duration,' ', -1) as Unidades \
        from dffilm \
        where release_year = "+anio+" and Id_Plataform = '"+p+"' and SUBSTRING_INDEX(duration,' ', -1) like 'Season%' \
        order by 4 desc \
        limit 1"
        cursor.execute(query)
    else:
        return "Inserte [min] o [season] en el tercer parametro"

    for dato in cursor:
        a.append(dato)
    
    return a
    


#2 Funcion que retorna  cantidad de Peliculas y series de la plataforma escogida
def cant(plataforma):
    cursor=conectar_a_base_de_datos()
    a=[]
    p=0
    if plataforma == "amazon":
        p = 1
    elif plataforma == "disney":
        p = 2
    elif plataforma == "hulu":
        p = 3
    elif plataforma == "netflix":
        p = 4
    else:
        "Inserte: amazon, disney, hulu o netflix"
    p=str(p)
    cursor.execute("SELECT Id_PLataform, type ,count(*) as Cantidad \
    FROM dffilm \
    where Id_Plataform = '"+p+"' \
    group by Id_Plataform, type")
    for dato in cursor:
        a.append(dato)
    
    return a
    
#3 Funcion que retorna la Plataforma con la mayor cantidad del genero insertado
def gen(genero):
    cursor=conectar_a_base_de_datos()
    a=[]
    query="SELECT Id_Plataform, listed_in, count(*) AS Cantidad\
    FROM dflisted \
    WHERE listed_in LIKE '"+genero+"' \
    GROUP BY Id_Plataform, listed_in \
    HAVING listed_in !='' \
    ORDER BY 3 DESC \
    LIMIT 1"
    cursor.execute(query)
    for dato in cursor:
        a.append(dato)
    
    return a
    

#4 Funcion que retorna el actor y la frecuencia con que se repite para el año y plataforma seleccionados
def act(plataforma,anio):
    cursor=conectar_a_base_de_datos()
    a=[]
    anio=str(anio)
    p=0
    if plataforma == "amazon":
        p = 1
    elif plataforma == "disney":
        p = 2
    elif plataforma == "hulu":
        p = 3
    elif plataforma == "netflix":
        p = 4
    else:
        "Inserte: amazon, disney, hulu o netflix"
    p=str(p)
    query="select Id_Plataform, cast, count(*) as Cantidad \
    from dfcast \
    where Id_plataform = '"+p+"' and Id_Producción like '"+anio+"%' \
    group by cast \
    having cast !='' \
    order by 3 desc \
    limit 1"
    cursor.execute(query)
    for dato in cursor:
        a.append(dato)
    
    return a

#uvicorn main:app --reload para iniciar servidor
@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/get_max_duration({anio},{plat},{minoseason})")  
async def maxduration(anio:int,plat:str,minoseason:str):
    if minoseason=="min":
        return {"La Pelicula con mas duración es ": max(anio,plat,minoseason)[0][0],
                "con una duración de" : max(anio,plat,minoseason)[0][4]}
    elif minoseason=="season":
        return {"La Serie con mas duración es ":max(anio,plat,minoseason)[0][0],
                "con una duración de" : max(anio,plat,minoseason)[0][4]}
    else:
        return {"Inserte sin o season en el tercer parametro"}

@app.get("/get_count_plataform({plat})") 
async def cantidadp(plat:str):
  
    return {"En la plataforma" : cant(plat)[0][0],
            "la cantidad de peliculas es" : cant(plat)[0][2],
            "la cantidad de series es" : cant(plat)[1][2]}

@app.get("/get_listedin({genero})") 
async def cantidadg(genero:str):
    return {"La Plataforma con mas cantidad de este genero es" : gen(genero)[0][0],
            "con una cantidad de" : gen(genero)[0][2]}

@app.get("/get_actor({plat},{anio})") 
async def actor(plat:str,anio:int):
    return {"El actor que mas se repite en esta plataforma es" : act(plat,anio)[0][1],
            "cuya cantidad es" : act(plat,anio)[0][4]}





