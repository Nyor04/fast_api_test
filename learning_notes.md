1) Cuando empece a estudiar referente a autenticacion en API tube que dar ciertos paseos por ciertas librerias y conocer 
   conceptos nuevos.

   por ejemplo la funcion especial "__call__" la cual dejare por aqui la investigacion:

   La función especial `__call__` en Python permite que una instancia de una clase se pueda "llamar" como si fuera una función. Cuando defines el método `__call__` en una clase, estás indicando cómo debería comportarse la instancia de la clase cuando se le llame con paréntesis.

Aquí tienes una explicación y un ejemplo:

### ¿Qué es `__call__`?
El método `__call__` es un método especial de Python que le da a un objeto la capacidad de comportarse como una función. Cuando este método está definido, puedes llamar a la instancia de la clase como si fuera una función. 

### ¿Cómo funciona `__call__`?
El método `__call__` se ejecuta automáticamente cuando llamas a una instancia de la clase. Esto puede ser útil cuando deseas que un objeto encapsule cierta funcionalidad que normalmente se manejaría a través de una función.

### Ejemplo básico de `__call__`
Imagina que tienes una clase que representa una calculadora simple que suma un número a un valor dado:

```python
class Suma:
    def __init__(self, incremento):
        self.incremento = incremento

    def __call__(self, x):
        return x + self.incremento

# Crear una instancia de la clase Suma
suma_5 = Suma(5)

# Llamar a la instancia como si fuera una función
resultado = suma_5(10)
print(resultado)  # Salida: 15
```

### Explicación
1. En el ejemplo, `Suma` es una clase que tiene un `incremento`.
2. La clase define el método `__call__`, que toma un argumento `x` y devuelve el resultado de sumar `x` y `incremento`.
3. Al crear `suma_5 = Suma(5)`, se crea un objeto que se puede llamar como una función.
4. Cuando llamamos `suma_5(10)`, Python ejecuta el método `__call__` de la instancia, y la salida es `15`.

### ¿Cuándo usar `__call__`?
Usar `__call__` es útil cuando quieres que una instancia de clase tenga un comportamiento funcional o si estás creando una clase que encapsula operaciones complejas pero quieres invocarla de una manera directa. Es común en patrones de diseño como el de "Funciones de Estado", donde las instancias de una clase representan diferentes comportamientos de una función. 


tambien aprendi sobre JWT:

Para trabajar con autenticación mediante JSON Web Tokens (JWT) en FastAPI, es fundamental comprender cómo funcionan los tokens JWT, su estructura y las implementaciones necesarias en FastAPI para proteger y autenticar los endpoints. Aquí tienes una guía completa de los aspectos que necesitas dominar:

### 1. **Conceptos Fundamentales de JWT**

   - **JWT** es un estándar para autenticar usuarios y mantener estados de sesión sin necesidad de almacenamiento en el servidor.
   - Está compuesto por tres partes separadas por puntos:
     - **Header**: Contiene el tipo de token y el algoritmo de firma.
     - **Payload**: Contiene la información o *claims* sobre el usuario o sesión.
     - **Signature**: Es la combinación del header y el payload firmada para asegurar la integridad del token.
   - **Firmas**: Puedes utilizar firmas HMAC (simétricas) o RSA (asimétricas), que permiten verificar la autenticidad del token.

### 2. **Configuración de FastAPI para JWT**

   Para implementar JWT en FastAPI necesitas:
   - La librería `pyjwt` para generar y decodificar los tokens JWT.
   - Configurar las variables de entorno, como `SECRET_KEY` y `ALGORITHM`, para firmar y verificar los tokens.
   - Definir tiempos de expiración del token (`access_token_expire_minutes`) para asegurar que los tokens no sean válidos indefinidamente.

   ```bash
   pip install pyjwt
   ```

### 3. **Creación y Verificación del Token**

   - **Generar el Token**:
     En un endpoint de autenticación (como `/login`), recibirás las credenciales, verificarás al usuario y generarás un JWT para la sesión.
   - **Verificar el Token**:
     Cada vez que un usuario accede a un endpoint protegido, verificarás el token JWT para autenticar su identidad.

   ```python
   from datetime import datetime, timedelta
   import jwt

   SECRET_KEY = "your_secret_key"
   ALGORITHM = "HS256"

   def create_access_token(data: dict, expires_delta: timedelta = None):
       to_encode = data.copy()
       if expires_delta:
           expire = datetime.utcnow() + expires_delta
       else:
           expire = datetime.utcnow() + timedelta(minutes=15)
       to_encode.update({"exp": expire})
       encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
       return encoded_jwt
   ```

### 4. **Endpoints de Autenticación: Login y Logout**

   - **Login**:
     1. Configura un endpoint de login que reciba las credenciales.
     2. Verifica las credenciales contra tu base de datos.
     3. Si son válidas, genera el JWT y lo devuelves al usuario.
   
   - **Logout** (Opcional):
     Aunque no es estrictamente necesario con JWT, puedes añadir un mecanismo para invalidar tokens.

### 5. **Protección de Endpoints con Dependencias** <---- ojo

   Usa el sistema de dependencias de FastAPI para proteger endpoints. Define una función de dependencia que verifique el JWT antes de permitir el acceso.

   ```python
   from fastapi import Depends, HTTPException, status
   from fastapi.security import OAuth2PasswordBearer
   from jose import JWTError, jwt

   oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

   async def get_current_user(token: str = Depends(oauth2_scheme)):
       credentials_exception = HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Could not validate credentials",
           headers={"WWW-Authenticate": "Bearer"},
       )
       try:
           payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
           username: str = payload.get("sub")
           if username is None:
               raise credentials_exception
       except JWTError:
           raise credentials_exception
       return username
   ```

### 6. **Buenas Prácticas de Seguridad**

   - **HTTPS**: Usa HTTPS para evitar la exposición de tokens (debido a que la comunicacion es cifrada)
   - **Cifrado de claves y secretos**: Usa `dotenv` o configuraciones de ambiente para proteger claves y secretos.

### Ejemplo Completo de Configuración

Un ejemplo básico de autenticación JWT en FastAPI incluye:
1. **Login** con generación de JWT.
2. **Protección de endpoints** con dependencias.


Este ejemplo previo es utiliza Oauth2 como modelo de autenticacion, cabe mencionar que he practicado solo con HTTP token bearer que es mandar el tokenJWT en el header del paquete HTTP.