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

    def cambiar_dificultad(e):
        problema = generar_problema(selector_dificultad.value)
        texto_problema.value = problema["problema"]
        pagina.respuesta_correcta = problema["respuesta"]
        campo_respuesta.value = ""
        feedback.value = ""
        pagina.update()

    selector_dificultad.on_change = cambiar_dificultad

    columna = ft.Column(
        [
            ft.Row([selector_dificultad], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(texto_problema, padding=10, bgcolor="#16213E", border_radius=10),
            campo_respuesta,
            boton_enviar,
            feedback
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER
    )

    pagina.add(columna)
    cambiar_dificultad(None)

ft.app(target=principal)