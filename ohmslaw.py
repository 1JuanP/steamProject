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

ft.app(target=principal)