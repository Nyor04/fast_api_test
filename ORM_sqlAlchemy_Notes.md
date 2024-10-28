**Descubriendo SQLalchemy ORM**

aunque la seccion se llame descubriendo en realidad ya conocia la libreria, pero nunca me habia dedicado a estudiarla.

una vez terminados temporalment mis estudios respecto a los metodos de autenticacion de la API, procedo a continuar mis estudios sobre los ORM, esta vez, con un alcance un poco mas profundo. Siendo  SQL alchemy el ORM a estudiar en esta ocacion. Tengo ciertos conocimientos previos, debido al Django ORM asi que tengo un buen punto de referencia.


**Contexto para estudios:**

Un **ORM (Object-Relational Mapper)** es una herramienta que permite interactuar con bases de datos relacionales usando un enfoque orientado a objetos (usando clases wey). En lugar de escribir consultas SQL directamente, el ORM permite manipular datos y esquemas de una base de datos mediante clases y métodos de un lenguaje de programación como Python. Así, el ORM convierte las acciones de código en operaciones SQL detrás de escena. Esto simplifica el trabajo con bases de datos y permite aprovechar el paradigma de la programación orientada a objetos.

**SQLAlchemy** es uno de los ORMs más utilizados en Python. Está dividido en dos partes principales:

1. **SQLAlchemy Core**: Proporciona herramientas para construir consultas SQL y ejecutar operaciones CRUD sin mucha abstracción. Permite un control más fino sobre las operaciones SQL.
   
2. **SQLAlchemy ORM**: Permite definir modelos de datos como clases de Python que se mapean a tablas en la base de datos. Con esta abstracción, las interacciones se realizan a través de instancias de estas clases, convirtiendo métodos como `save()` o `delete()` en sentencias SQL sin necesidad de escribirlas directamente.

Con SQLAlchemy, se pueden manejar esquemas de base de datos complejos, ejecutar consultas avanzadas, y también migrar la estructura de datos a medida que evoluciona la aplicación.