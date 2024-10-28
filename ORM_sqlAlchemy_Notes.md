**Descubriendo SQLalchemy ORM**

aunque la seccion se llame descubriendo en realidad ya conocia la libreria, pero nunca me habia dedicado a estudiarla.

una vez terminados temporalment mis estudios respecto a los metodos de autenticacion de la API, procedo a continuar mis estudios sobre los ORM, esta vez, con un alcance un poco mas profundo. Siendo  SQL alchemy el ORM a estudiar en esta ocacion. Tengo ciertos conocimientos previos, debido al Django ORM asi que tengo un buen punto de referencia.


**Contexto para estudios:**

Un **ORM (Object-Relational Mapper)** es una herramienta que permite interactuar con bases de datos relacionales usando un enfoque orientado a objetos (usando clases wey). En lugar de escribir consultas SQL directamente, el ORM permite manipular datos y esquemas de una base de datos mediante clases y métodos de un lenguaje de programación como Python. Así, el ORM convierte las acciones de código en operaciones SQL detrás de escena. Esto simplifica el trabajo con bases de datos y permite aprovechar el paradigma de la programación orientada a objetos.

**SQLAlchemy** es uno de los ORMs más utilizados en Python. Está dividido en dos partes principales:

1. **SQLAlchemy Core**: Proporciona herramientas para construir consultas SQL y ejecutar operaciones CRUD sin mucha abstracción. Permite un control más fino sobre las operaciones SQL.
   
2. **SQLAlchemy ORM**: Permite definir modelos de datos como clases de Python que se mapean a tablas en la base de datos. Con esta abstracción, las interacciones se realizan a través de instancias de estas clases, convirtiendo métodos como `save()` o `delete()` en sentencias SQL sin necesidad de escribirlas directamente.

Con SQLAlchemy, se pueden manejar esquemas de base de datos complejos, ejecutar consultas avanzadas, y también migrar la estructura de datos a medida que evoluciona la aplicación.


¡Claro, vamos paso a paso con SQLAlchemy! Ahora que tenemos una base sobre ORM y vimos el propósito de SQLAlchemy, enfoquémonos en las características iniciales que te serán útiles. Primero, cubriremos los elementos básicos de SQLAlchemy para que puedas comprender cómo conectar, crear y manipular bases de datos a nivel de objetos.

### 1. **Configuración de SQLAlchemy y Conexión a una Base de Datos**
SQLAlchemy admite una variedad de bases de datos (como SQLite, PostgreSQL, MySQL, etc.), y permite conectarse mediante una engine. 

El "engine" se encarga de gestionar las conexiones y ejecutar comandos SQL en la base de datos.

```python
from sqlalchemy import create_engine

# Ejemplo de conexión a una base de datos SQLite
engine = create_engine('sqlite:///mi_base_datos.db') #ejemplo de conexion a base de datos sqlite
```

### 2. **Mapeo de Clases a Tablas (Declarative Base)**
SQLAlchemy permite definir las tablas como clases en Python mediante el uso de `Declarative Base`, que es el núcleo de la creación de modelos en SQLAlchemy. `Declarative Base` permite que una clase represente una tabla de la base de datos, donde cada atributo de la clase representa una columna de la tabla, por lo visto, el concepto es el mismo que en DJANGO.

```python
from sqlalchemy import Column, Integer, String # se importan los tipos de datos a usar en las tablas
from sqlalchemy.orm import declarative_base

# Crear base declarativa
Base = declarative_base()

# Definir una tabla como clase
class Usuario(Base):
    __tablename__ = 'usuarios'  # Nombre de la tabla en la base de datos
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String, unique=True)
```

### 3. **Creación de la Tabla**
Una vez que defines las clases, puedes crear las tablas en la base de datos directamente desde Python.

```python
# Crea las tablas en la base de datos
Base.metadata.create_all(engine)
```

### 4. **Sesiones (Sessions)**
Las sesiones son esenciales en SQLAlchemy. Administran las transacciones y permiten realizar operaciones de consulta, inserción, actualización y eliminación (CRUD). 

```python
from sqlalchemy.orm import sessionmaker

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()
```

### 5. **Inserción de Datos**
Con una sesión activa, ahora puedes agregar instancias de tus modelos a la base de datos.

```python
nuevo_usuario = Usuario(nombre="Carlos", email="carlos@ejemplo.com")
session.add(nuevo_usuario)  # Agregar el objeto a la sesión
session.commit()  # Guardar cambios en la base de datos
```

### 6. **Consultas Básicas**
Las consultas se ejecutan directamente en la sesión y devuelven instancias de las clases que definiste.

```python
# Obtener todos los usuarios
usuarios = session.query(Usuario).all()
for usuario in usuarios:
    print(usuario.nombre, usuario.email)
```

### Próximos Pasos:
- Explorar consultas avanzadas con filtros y condiciones.
- Trabajar con relaciones entre tablas (relaciones de uno a muchos, muchos a muchos).
- Implementar transacciones y manejo de errores.



Termine estudiando un concepto de base de datos bastante interesante: **Transacciones**

Una **transacción** en el contexto de bases de datos es una secuencia de una o varias operaciones (como `INSERT`, `UPDATE`, `DELETE`) que se ejecutan como una unidad indivisible. Las transacciones aseguran que todas las operaciones se completen exitosamente o ninguna se ejecute, manteniendo la **integridad** y **consistencia** de los datos en la base de datos.

Las transacciones cumplen con el principio **ACID**, que define sus características principales:

1. **Atomicidad**: La transacción debe completarse en su totalidad; si alguna operación falla, ninguna operación de la transacción debería aplicarse.
  
2. **Consistencia**: Las transacciones deben llevar la base de datos de un estado válido a otro, respetando las reglas y restricciones establecidas.

3. **Aislamiento**: Cada transacción debe ser independiente de las demás y no debería interferir con otras transacciones que se estén ejecutando al mismo tiempo.
  
4. **Durabilidad**: Una vez que la transacción se completa, los cambios son permanentes y se mantendrán incluso en caso de fallo del sistema.

### Ejemplo práctico en SQLAlchemy

En SQLAlchemy, podrías trabajar con transacciones usando un **contexto de sesión** para ejecutar varias operaciones y, al final, **confirmarlas** o **revertirlas** si ocurre un error:

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Crear el motor y la sesión
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)

# Ejecutar una transacción
session = Session()
try:
    # Operaciones de la transacción
    user = User(name="Alice", age=30)
    session.add(user)
    session.commit()  # Confirma la transacción
except:
    session.rollback()  # Revierte la transacción en caso de error
    print("Error en la transacción")
finally:
    session.close()
```

Este proceso ayuda a proteger la base de datos de errores, asegurando que los cambios solo se apliquen si todas las operaciones de la transacción tienen éxito.