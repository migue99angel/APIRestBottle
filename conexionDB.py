from bottle import Bottle
from bottle_login import LoginPlugin
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql://root:secret@localhost:33060/Prueba')
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
        results.append({'id':x.name})

    return {'table_data' : results}

app.run(debug = True,reloader=True)