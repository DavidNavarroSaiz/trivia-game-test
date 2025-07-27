from fastapi import FastAPI, Body
import uvicorn
from leer_trivia import cargar_preguntas, obtener_pregunta_por_id

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Trivia Game",
    description="Una API simple para manejar preguntas de trivia",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """
    Endpoint principal - página de bienvenida
    """
    return {
        "mensaje": "¡Bienvenido a la API de Trivia Game!",
        "endpoints_disponibles": {
            "listar_preguntas": "GET /list_questions",
            "obtener_pregunta_por_id": "GET /question/{question_id}",
            "verificar_respuesta": "POST /verify_answer/{question_id}",
            "agregar_pregunta": "POST /add_question",
            "actualizar_pregunta": "PUT /update_question",
            "eliminar_pregunta": "DELETE /delete_question"
        }
    }


@app.post("/add_question")
def add_question():
    """
    Endpoint para agregar una nueva pregunta (aún no implementado)
    """
    return {"mensaje": "Función para agregar pregunta - pendiente de implementar"}

@app.put("/update_question")
def update_question():
    """
    Endpoint para actualizar una pregunta existente (aún no implementado)
    """
    return {"mensaje": "Función para actualizar pregunta - pendiente de implementar"}


@app.delete("/delete_question")
def delete_question():
    """
    Endpoint para eliminar una pregunta (aún no implementado)
    """
    return {"mensaje": "Función para eliminar pregunta - pendiente de implementar"}

@app.get("/list_questions")
def list_questions():
    """
    Endpoint para obtener todas las preguntas del archivo JSON
    """
    try:
        # Cargar las preguntas desde el archivo JSON
        preguntas = cargar_preguntas('trivia_questions.json')
        
        if not preguntas:
            return {
                "error": "No se pudieron cargar las preguntas", 
                "preguntas": []
            }
        
        return {
            "mensaje": f"Se cargaron {len(preguntas)} preguntas exitosamente",
            "total_preguntas": len(preguntas),
            "preguntas": preguntas
        }
    except Exception as e:
        return {
            "error": f"Error al cargar las preguntas: {str(e)}",
            "preguntas": []
        }

@app.get("/question/{question_id}")
def get_question_by_id(question_id: int):
    """
    Endpoint para obtener una pregunta específica por su ID
    """
    try:
        # Cargar las preguntas desde el archivo JSON
        preguntas = cargar_preguntas('trivia_questions.json')
        
        if not preguntas:
            return {
                "error": "No se pudieron cargar las preguntas",
                "pregunta": None
            }
        
        # Buscar la pregunta específica por ID
        pregunta = obtener_pregunta_por_id(preguntas, question_id)
        
        if pregunta is None:
            return {
                "error": f"No se encontró una pregunta con el ID {question_id}",
                "pregunta": None,
                "ids_disponibles": [p['id'] for p in preguntas]
            }
        
        return {
            "mensaje": f"Pregunta con ID {question_id} encontrada exitosamente",
            "pregunta": pregunta
        }
        
    except Exception as e:
        return {
            "error": f"Error al obtener la pregunta: {str(e)}",
            "pregunta": None
        }

@app.post("/verify_answer/{question_id}")
def verify_answer(question_id: int, user_answer: int = Body(..., description="Respuesta del usuario (0-3)")):
    """
    Endpoint para verificar si la respuesta del usuario es correcta
    """
    try:
        # Cargar las preguntas desde el archivo JSON
        preguntas = cargar_preguntas('trivia_questions.json')
        
        if not preguntas:
            return {
                "error": "No se pudieron cargar las preguntas",
                "resultado": None
            }
        
        # Buscar la pregunta específica por ID
        pregunta = obtener_pregunta_por_id(preguntas, question_id)
        
        if pregunta is None:
            return {
                "error": f"No se encontró una pregunta con el ID {question_id}",
                "resultado": None,
                "ids_disponibles": [p['id'] for p in preguntas]
            }
        
        # Validar que la respuesta del usuario esté en el rango válido
        if user_answer < 0 or user_answer >= len(pregunta['opciones']):
            return {
                "error": f"Respuesta inválida. Debe ser un número entre 0 y {len(pregunta['opciones']) - 1}",
                "resultado": None,
                "opciones_disponibles": pregunta['opciones']
            }
        
        # Verificar si la respuesta es correcta
        respuesta_correcta = pregunta['respuesta_correcta']
        es_correcta = user_answer == respuesta_correcta
        
        # Preparar la respuesta
        resultado = {
            "pregunta_id": question_id,
            "respuesta_usuario": user_answer,
            "respuesta_correcta": respuesta_correcta,
            "es_correcta": es_correcta,
            "opcion_usuario": pregunta['opciones'][user_answer],
            "opcion_correcta": pregunta['opciones'][respuesta_correcta]
        }
        
        return {
            "mensaje": "Respuesta verificada exitosamente",
            "resultado": resultado
        }
        
    except Exception as e:
        return {
            "error": f"Error al verificar la respuesta: {str(e)}",
            "resultado": None
        }


# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    print("🚀 Iniciando servidor FastAPI...")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🌐 API disponible en: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)