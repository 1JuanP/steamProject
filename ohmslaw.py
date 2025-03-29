import random
import flet as ft

def generar_problema(dificultad):
    if dificultad == 'Fácil':
        V = random.randint(1, 20)
        R = random.randint(1, 20)
        I = round(V / R, 2)
        variable = random.choice(['V', 'I', 'R'])
        if variable == 'V':
            return {"problema": f"Circuito: I={I}A, R={R}Ω. ¿Voltaje?", "respuesta": V}
        elif variable == 'I':
            return {"problema": f"Circuito: V={V}V, R={R}Ω. ¿Corriente?", "respuesta": I}
        else:
            return {"problema": f"Circuito: V={V}V, I={I}A. ¿Resistencia?", "respuesta": R}
    elif dificultad == 'Medio':
        R1 = random.randint(1, 10)
        R2 = random.randint(1, 10)
        V = random.randint(10, 50)
        combo = random.choice(['serie', 'paralelo'])
        if combo == 'serie':
            Req = R1 + R2
            return {"problema": f"Resistencias: R1={R1}Ω, R2={R2}Ω (serie) con V={V}V. ¿Corriente?", "respuesta": round(V/Req, 2)}
        else:
            Req = round((R1*R2)/(R1+R2), 2)
            return {"problema": f"Resistencias: R1={R1}Ω, R2={R2}Ω (paralelo) con V={V}V. ¿Corriente?", "respuesta": round(V/Req, 2)}
    elif dificultad == 'Difícil':
        V = random.randint(20, 100)
        R = random.randint(10, 50)
        return {"problema": f"Circuito: V={V}V, R={R}Ω. ¿Potencia disipada?", "respuesta": round((V**2)/R, 2)}

def principal(pagina: ft.Page):
    pagina.title = "Resolvedor de Física de la Ley de Ohm"
    pagina.theme_mode = ft.ThemeMode.DARK
    pagina.bgcolor = "#1A1A2E"
    pagina.padding = 20
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    selector_dificultad = ft.Dropdown(
        options=[
            ft.dropdown.Option("Fácil"),
            ft.dropdown.Option("Medio"),
            ft.dropdown.Option("Difícil")
        ],
        value="Fácil",
        width=200,
        bgcolor="#16213E",
        border_radius=10,
        color="#E0E0E0"
    )

    texto_problema = ft.Text(size=16, weight=ft.FontWeight.BOLD, color="#E0E0E0")
    campo_respuesta = ft.TextField(label="Tu respuesta", width=200, bgcolor="#16213E", border_radius=10)
    boton_enviar = ft.ElevatedButton("Enviar", bgcolor="#0F3460", color="#E0E0E0")
    feedback = ft.Text()
    indicador_dificultad = ft.Icon(ft.icons.CIRCLE, color=ft.colors.GREEN)

    def cambiar_dificultad(e):
        dificultad = selector_dificultad.value
        problema = generar_problema(dificultad)
        texto_problema.value = problema["problema"]
        pagina.respuesta_correcta = problema["respuesta"]
        campo_respuesta.value = ""
        feedback.value = ""
        
        if dificultad == "Fácil":
            indicador_dificultad.color = ft.colors.GREEN
        elif dificultad == "Medio":
            indicador_dificultad.color = ft.colors.YELLOW
        else:
            indicador_dificultad.color = ft.colors.RED
            
        pagina.update()

    def verificar_respuesta(e):
        try:
            respuesta = float(campo_respuesta.value)
            if abs(respuesta - pagina.respuesta_correcta) < 0.06:
                feedback.value = "¡Correcto! ⚡"
                feedback.color = ft.colors.GREEN
            else:
                feedback.value = f"Incorrecto. Respuesta: {pagina.respuesta_correcta}"
                feedback.color = ft.colors.RED
        except ValueError:
            feedback.value = "Ingresa un número válido"
            feedback.color = ft.colors.ORANGE
        pagina.update()

    selector_dificultad.on_change = cambiar_dificultad
    boton_enviar.on_click = verificar_respuesta

    columna = ft.Column(
        [
            ft.Row([
                ft.Text("Dificultad:"),
                selector_dificultad,
                indicador_dificultad
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(texto_problema, padding=10, bgcolor="#16213E", border_radius=10),
            campo_respuesta,
            boton_enviar,
            feedback
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        width=400
    )

    pagina.add(columna)
    cambiar_dificultad(None)

ft.app(target=principal)