# API REST: Interfaz de programacion de aplicaciones para compartir recursos.

from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Se inicializa una variable donde tendra todas las caracteristicas de una API REST
app = FastAPI()

#Se define el modelo a usar
class Curso(BaseModel):
    id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Se simula una base de datos temporal.
cursos_db = []

# CRUD: Read(Lectura) se utiliza el metodo GET ALL: el cual leera todos los cursos que halla en la base de datos
@app.get("/cursos/", response_model=List[Curso])
def obtener_cursos():
    return cursos_db

# CRUD: Create(Escribir) se utiliza el metodo POST: el cual agregara un nuevo curso en la base de datos
@app.post("/cursos/", response_model=Curso)
def crear_curso(curso:Curso):
    curso.id = str(uuid.uuid4()) # Usamos UUID para generar un ID único e irrepetible
    cursos_db.append(curso)
    return curso

# CRUD: Read(Lectura) se utiliza el metodo GET de forma individual: el cual leera el curso que coincida con el ID que pidamos
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array devuelto
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

#CRUD: Update(Actualizar/modificar) se utiliza el metodo PUT: el cual actualiza o modifica un recurso que coincida con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coincidencia
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # buscamos el indece exacto donde esta el curso en la base de datos
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# CRUD: Delete(Eliminar) se utiliza el metodo DELETE para eliminar un curso que coincida con el ID que mandemos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # con next tomamos la primera coincidencia
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
