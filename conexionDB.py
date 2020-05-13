from bottle import Bottle
from bottle_login import LoginPlugin
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://miguelAngel:practicasSIBW@127.0.0.1:3306/Prueba')
app = Bottle()
plugin = sqlalchemy.Plugin(engine,keyword='db')
app.install(plugin)

class MiTabla(Base):
    __tablename__ = 'MiTabla'
    id = Column(Integer, primary_key=True)

@app.get('/')
def show(db):
    table_data = db.query(MiTabla)

    results = []
    for x in table_data:
        results.append({'id':x.id})

    return {'table_data' : results}

port = 5000
host = "localhost"
app.run(debug = True,reloader=True, host=host, port=port)
