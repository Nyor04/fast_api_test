from fastapi import Response, FastAPI#importar la clase de fastAPI es el primer paso para poder usar el framework.
from typing import Union
app = FastAPI() #crear una instancia de la clase FastAPI es el segundo paso para poder usar el framework.

@app.get("/") #cuando en nuestra aplicacion se haga un get request hacia la URL que indiquemos en el argumento del decorador
def read_root():#<--- se ejecutara esta funcion 
    return {'message':'hello World!'} # para este ejemplo, deberia retornar un Hello world.


#interaccion con la API: se puede tener rutas dinamicas usando placeholders, estos van en llaves. los valores puestos aca son dinamicos como Pks.
@app.get("/items/{item_id}")#<-- estos place holders se les conoce como parametros de ruta.
def read_item(item_id:int): #<-- el parametro de ruta tomado de la url pasa como argumento a la funcion a ejecutar cuando se llama la url (en este caso /items/{item_id})
    return {'item_id':item_id} # retornando el json como de costumbre.





#parametros de busqueda.
@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10): #<--- declarar parametros en la funcion a ejecutar cuando se hace un get request a la URL se le conocen como parametros de busqueda. es como hacer querys en la URL usando "?" como indicador de un parametro para luego darle un valor.
    return {'skip':skip,
            'limit':limit
            }

'''
Ejemplo :http://127.0.0.1:8000/items/?skip=10&limit=20, recibirás:


{
    "skip": 10,
    "limit": 20
}
Ejemplo :http://127.0.0.1:8000/items/, en teoria recibes recibirás:


{
    "skip": 0,
    "limit": 10
}

debido a que son valores por defecto de estos parametros.
'''



#para dar respuestas personalizadas se debe importar la clase response de la libreria de fastapi
@app.get("/custom_response/{uname}")
def get_custom_response(uname:str):
    message = f'Hola {uname}, esta es una respuesta personalizada de FAST API.'
    return Response(content=message, media_type="text/plain")
#recibimos un string en el parametro {uname}, el cual debe ser uns tring para luego insertar dicho string en un
#mensaje de respuesta personalizado, favor notar que se debe indicar el media type y pasar el atributo content, el charset por defecto es utf-8.