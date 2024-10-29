

# Bitácora de Aprendizaje de FastAPI

Este repositorio contiene pruebas para experimentar con las funcionalidades que ofrece **FastAPI**. Aquí registraré lo que vaya aprendiendo para llevar un control de mi progreso.

### 1. Primeros pasos con FastAPI

#### Importar FastAPI
El primer paso para utilizar FastAPI es importar la clase **FastAPI**:

```python
from fastapi import FastAPI
```

#### Crear una instancia de FastAPI
El segundo paso es crear una instancia de la clase FastAPI:

```python
app = FastAPI()
```

### 2. Creando la primera ruta

Puedes crear rutas utilizando decoradores de Python. Por ejemplo, para una ruta GET en la raíz de la aplicación (`"/"`):

```python
@app.get("/") 
def read_root():
    return {'message': 'Hello World!'}
```

Cuando se haga una solicitud GET hacia la URL especificada en el decorador, se ejecutará la función `read_root`, y devolverá el mensaje `"Hello World!"`.

---

### 3. Parámetros de ruta

#### Rutas dinámicas con parámetros de ruta
Puedes definir rutas dinámicas usando **placeholders** que van entre llaves `{}`. Estos valores dinámicos pueden ser claves primarias (PKs) o cualquier otro valor. Se les conoce como **parámetros de ruta**.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {'item_id': item_id}
```

En este ejemplo, el parámetro `item_id` es parte de la URL y será pasado a la función `read_item` cuando la ruta sea accedida. El valor será retornado en un JSON.

---

### 4. Parámetros de consulta (Query Parameters)

#### Definir parámetros de consulta
Puedes usar **parámetros de consulta** para filtrar o limitar los resultados de una solicitud.

```python
@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return {'skip': skip, 'limit': limit}
```

- **`skip`**: Número de elementos a omitir.
- **`limit`**: Máximo número de elementos a devolver.

**Ejemplo de uso:**

- **URL**: `http://127.0.0.1:8000/items/?skip=10&limit=20`
  - **Respuesta:**

    ```json
    {
      "skip": 10,
      "limit": 20
    }
    ```

- **URL**: `http://127.0.0.1:8000/items/`
  - **Respuesta:**

    ```json
    {
      "skip": 0,
      "limit": 10
    }
    ```

En este caso, se devuelven los valores por defecto para los parámetros de consulta (`skip = 0`, `limit = 10`).

---

### 5. Documentación automática de la API

FastAPI genera automáticamente la documentación de tu API.

- **Swagger UI**: Disponible en la ruta `"/docs"`. Te permite explorar y probar las rutas directamente desde el navegador.
  
- **ReDoc**: Otra documentación visual, disponible en `"/redoc"`, aunque **Swagger** es generalmente más interactivo.

---

### 6. Validación automática con Pydantic

FastAPI usa **Pydantic** para validar los datos que envías a la API de manera automática. Pydantic es una librería para la validación de datos (consulta más detalles en [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)).

Por ejemplo, si envías una cadena en lugar de un número para un parámetro que espera un `float`, recibirás un error de validación:

```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "value is not a valid float",
      "type": "type_error.float"
    }
  ]
}
```

Este tipo de validación es automática y evita errores en la API causados por datos incorrectos.

---

Con esto, hemos cubierto algunas de las funcionalidades básicas de FastAPI. Continuaré actualizando esta bitácora a medida que aprenda más sobre el framework y sus características avanzadas.

