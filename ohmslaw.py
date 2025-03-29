import flet as ft

def principal(pagina: ft.Page):
    pagina.title = "Resolvedor de Física de la Ley de Ohm"
    pagina.theme_mode = ft.ThemeMode.DARK
    pagina.bgcolor = "#1A1A2E"
    pagina.padding = 20
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

ft.app(target=principal)