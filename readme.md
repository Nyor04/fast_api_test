


# The Anything API

Este es un proyecto de ejemplo para una API en Python, puse a prueba varios conceptosque ofrece este framework.

lo que mas puedo resaltar es: 

- Comprendi el flujo de trabajo de fastAPI
- Me enamore de pydantic
- Typer es cool
- SQLAlchemy es bastante hermoso.
- Toque ligeramente conceptos de autenticacion, especialmente JWT Token bearer
- API routes
- Concepto de API Services 
- Practique la modularizacion del proyecto

en realidad estoy muy feliz con todo el contenido que aprendi en esta investigacion quiza en un futuro haga mas actualizaciones
10-29-2024.


## Requisitos

- **Python 3.8+**: Asegúrate de tener Python instalado en tu sistema. Puedes verificar la versión de Python con el siguiente comando:

  ```bash
  python --version
  ```


## Pasos para la instalación

### 1. Clona el repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/Nyor04/fast_api_test.git
cd fast_api_test
```

### 2. Crea un entorno virtual

Es recomendable usar un entorno virtual para evitar conflictos de dependencias:

```bash
python -m venv env
```

Activa el entorno virtual:

- En Windows:

  ```bash
  .\env\Scripts\activate
  ```

- En macOS y Linux:

  ```bash
  source env/bin/activate
  ```

### 3. Instala las dependencias

Las dependencias están listadas en `requirements.py`. Instálalas ejecutando:

```bash
pip install -r requirements.py
```

### 4. Configura las variables de entorno

Crea un archivo `.env` en el directorio raíz del proyecto. Este archivo almacenará las variables de entorno requeridas para la autenticación JWT. Abre el archivo `.env` y agrega las siguientes variables:

```plaintext
SECRET_KEY="your_secret_key"
ALGORITHM="HS256"
```

> **Nota**: Asegúrate de revisar el archivo `middlewares/jwt_manager.py` para obtener más contexto sobre los valores de `SECRET_KEY` y `ALGORITHM`.

### 5. Ejecuta el proyecto localmente

Para ejecutar la API localmente, usa **Uvicorn**:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en `http://127.0.0.1:8000` con recarga automática de código.

## Despliegue

Si deseas hacer un despliegue en plataformas como GitLab o GitHub Actions, necesitarás configurar el proceso de CI/CD según tus preferencias. Asegúrate de gestionar de forma segura las variables de entorno en el entorno de despliegue.

---

¡Listo! Ahora deberías poder instalar y ejecutar el proyecto tanto en local como en entornos remotos.
happy Coding (❁´◡`❁)


