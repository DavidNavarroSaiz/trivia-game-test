import json

def cargar_preguntas(file_name):
    """Carga las preguntas desde el archivo JSON"""
    try:
        with open(file_name, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            
            return datos['preguntas']
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_name}'")
        return []
    except json.JSONDecodeError:
        print("Error: El archivo JSON no tiene un formato válido")
        return []

def obtener_pregunta_por_id(preguntas, id_pregunta):
    """Obtiene una pregunta específica por su ID"""
    for pregunta in preguntas:
        if pregunta['id'] == id_pregunta:
            return pregunta
    return None

def mostrar_pregunta_por_id(preguntas, id_pregunta):
    """Muestra una pregunta específica por su ID y permite responderla"""
    pregunta = obtener_pregunta_por_id(preguntas, id_pregunta)
    
    if pregunta is None:
        print(f"❌ No se encontró una pregunta con el ID {id_pregunta}")
        return False
    
    print(f"\n{'='*50}")
    print(f"Pregunta #{pregunta['id']} - {pregunta['categoria']}")
    print(f"{'='*50}")
    print(f"Pregunta: {pregunta['pregunta']}")
    print("\nOpciones:")
    
    for i, opcion in enumerate(pregunta['opciones']):
        print(f"  {i+1}. {opcion}")

    # Obtener respuesta del usuario
    respuesta_usuario = obtener_respuesta_usuario(pregunta['opciones'])
    respuesta_correcta = pregunta['respuesta_correcta']
    
    # Validar respuesta
    if respuesta_usuario == respuesta_correcta:
        print("✅ ¡Correcto!")
        return True
    else:
        print("❌ Incorrecto!")
        print(f"La respuesta correcta era: {respuesta_correcta + 1}. {pregunta['opciones'][respuesta_correcta]}")
        return False

def obtener_respuesta_usuario(opciones):
    """Obtiene y valida la respuesta del usuario (número o palabra)"""
    while True:
        try:
            respuesta = input("\nTu respuesta (número 1-4 o palabra): ").strip().lower()
            
            # Verificar si es un número válido
            if respuesta in ['1', '2', '3', '4']:
                return int(respuesta) - 1  # Convertir a índice (0-3)
            
            # Verificar si es una palabra que coincide con alguna opción
            for i, opcion in enumerate(opciones):
                if respuesta == opcion.lower():
                    return i
            
            # Si no coincide con nada, mostrar error
            print("❌ Por favor, ingresa un número del 1 al 4 o escribe la palabra exacta de una de las opciones.")
            
        except ValueError:
            print("❌ Por favor, ingresa un número válido o una palabra.")

def mostrar_pregunta(pregunta):
    """Muestra una pregunta individual con sus opciones y valida la respuesta"""
    print(f"\n{'='*50}")
    print(f"Pregunta #{pregunta['id']} - {pregunta['categoria']}")
    print(f"{'='*50}")
    print(f"Pregunta: {pregunta['pregunta']}")
    print("\nOpciones:")
    
    for i, opcion in enumerate(pregunta['opciones']):
        print(f"  {i+1}. {opcion}")

    # Obtener respuesta del usuario
    respuesta_usuario = obtener_respuesta_usuario(pregunta['opciones'])
    respuesta_correcta = pregunta['respuesta_correcta']
    
    # Validar respuesta
    if respuesta_usuario == respuesta_correcta:
        print("✅ ¡Correcto!")
        return True
    else:
        print("❌ Incorrecto!")
        # print(f"La respuesta correcta era: {respuesta_correcta + 1}. {pregunta['opciones'][respuesta_correcta]}")
        return False

def main():
    """Función principal del programa"""
    print("🎯 JUEGO DE TRIVIA - LECTOR DE PREGUNTAS")
    print("=" * 50)
    
    # Cargar las preguntas
    preguntas = cargar_preguntas('trivia_questions.json')
    if not preguntas:
        print("No se pudieron cargar las preguntas.")
        return
    
    print(f"Se cargaron {len(preguntas)} preguntas exitosamente.\n")
    
    # Menú de opciones
    while True:
        print("\n¿Qué quieres hacer?")
        print("1. Jugar todas las preguntas")
        print("2. Jugar una pregunta específica por ID")
        print("3. Salir")
        
        opcion = input("\nElige una opción (1-3): ").strip()
        
        if opcion == "1":
            jugar_todas_las_preguntas(preguntas)
        elif opcion == "2":
            jugar_pregunta_especifica(preguntas)
        elif opcion == "3":
            print("¡Gracias por jugar! 👋")
            break
        else:
            print("❌ Opción no válida. Por favor, elige 1, 2 o 3.")

def jugar_todas_las_preguntas(preguntas):
    """Juega todas las preguntas del trivia"""
    print(f"\n{'='*50}")
    print("🎮 JUGANDO TODAS LAS PREGUNTAS")
    print(f"{'='*50}")
    
    # Variables para el puntaje
    puntaje = 0
    total_preguntas = len(preguntas)
    print(f"Total de preguntas: {total_preguntas}")
    
    # Mostrar todas las preguntas y validar respuestas
    for pregunta in preguntas:
        if mostrar_pregunta(pregunta):
            puntaje += 1
    
    # Mostrar resultado final
    print(f"\n{'='*50}")
    print("🎉 ¡JUEGO TERMINADO!")
    print(f"{'='*50}")
    print(f"Puntaje final: {puntaje}/{total_preguntas}")
    print(f"Porcentaje de aciertos: {(puntaje/total_preguntas)*100:.1f}%")
    
    if puntaje == total_preguntas:
        print("🏆 ¡Perfecto! ¡Obtuviste todas las respuestas correctas!")
    elif puntaje >= total_preguntas * 0.8:
        print("🌟 ¡Excelente trabajo!")
    elif puntaje >= total_preguntas * 0.6:
        print("👍 ¡Buen trabajo!")
    else:
        print("📚 ¡Sigue estudiando!")

def jugar_pregunta_especifica(preguntas):
    """Juega una pregunta específica por ID"""
    print(f"\n{'='*50}")
    print("🎯 JUGANDO PREGUNTA ESPECÍFICA")
    print(f"{'='*50}")
    
    # Mostrar IDs disponibles
    print("IDs de preguntas disponibles:")
    for pregunta in preguntas:
        print(f"  ID {pregunta['id']}: {pregunta['categoria']}")
    
    # Obtener ID del usuario
    while True:
        try:
            id_pregunta = int(input("\nIngresa el ID de la pregunta que quieres jugar: "))
            break
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
    
    # Jugar la pregunta específica
    mostrar_pregunta_por_id(preguntas, id_pregunta)

if __name__ == "__main__":
    main() 