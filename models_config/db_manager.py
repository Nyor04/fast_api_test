

from sqlalchemy import create_engine # create_engine es el Core de sqlalchemy, te permite crear los motores o conectores a las bases de datos
from sqlalchemy.orm import sessionmaker, declarative_base 
from os import path
#session maker te permite crear una "session" con la DB, hazta el momento la interpreto como una transaccion.
#declarative_base es lo que permite crear clases de python que seran transformadas en tablas de DBs. se debe almacenar el resultado de la funcion en una variable y pasar esta variable como argumento de una clase que creemos para que herede las caracteristicas del ORM (creo.)
base_dir = path.dirname(path.realpath(__file__))
sqlite_file_name = "../mockDB.sqlite3"
db_url = f"sqlite:///{path.join(base_dir, sqlite_file_name)}"

engine = create_engine(
    db_url,
    echo=True, #imprime los SQL statement en la consola.
    connect_args={"check_same_thread": False}
)

Base = declarative_base()

Session = sessionmaker(bind=engine) # se crea una instancia de sessionmaker (wtf, nombre de clase con minuscula XD)




"""
class Usuarios(Base):
    __tablename__ = "usuarios" # el nombre de la tabla se define con la funcion especial __tablename__ (creo que es una funcion especial custom, investigar luego.)
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String, unique=True)

Base.metadata.create_all(engine) #esto crea la base de datos


'''
Una vez se tiene una Sesion abierta se puede empezar a desarrollar la logica de interaccion con la DB.
para este ejemplo, creare un usuario nuevo, esto lo lograre creando unas instancia de la clase Usuarios, en donde solo le pasare los atributos nombre y email. 

luego se debe de agregar a la sesion con el metodo add y para guardar pues se usa un commit (git?)
'''
nuevo_pibe = Usuarios(nombre="happy Dev", email="evilBryan@devtest.com")
Tsession.add(nuevo_pibe)
Tsession.commit()



Para hacer querys, (al menos el mas sencillo se usa el metodo query de la session, en este caso Tsession), este metodo recibe como parametro el la clase a la cual se va a hacer el query (recordando que en los ORM la clase representa una tabla en la base de datos.) para posterior usar el metodo all (que asumo que retorna todas las entradas de la tabla en la DB)

usuarios = Tsession.query(Usuarios).all()
for usuario in usuarios:
    print(usuario.nombre, usuario.email)

"""
