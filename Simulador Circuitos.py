import flet as ft

def welcome_page(page: ft.Page):
    title = ft.Text("Bienvenido al Simulador de Circuitos", size=24, weight=ft.FontWeight.BOLD)
    description = ft.Text(
        "Este simulador te permite agregar resistencias y capacitores en serie o paralelo "
        "y calcular la resistencia y capacitancia equivalentes del circuito.",
        size=16
    )
    instructions = ft.Text("Para comenzar, haz clic en el botón 'Iniciar Simulador'.", size=14)
    image1 = ft.Image(src="image1.jpg", width=200, height=100)
    image2 = ft.Image(src="image2.jpg", width=200, height=100)

    def start_simulator(e):
        page.controls.clear()
        simulator_page(page)

    start_button = ft.ElevatedButton("Iniciar Simulador", on_click=start_simulator)

    content = ft.Column(
        controls=[
            title,
            description,
            ft.Row([image1, image2], alignment=ft.MainAxisAlignment.CENTER),
            instructions,
            start_button
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    page.add(content)

def main(page: ft.Page):
    page.title = "Simulador de Circuitos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    welcome_page(page)

ft.app(target=main, assets_dir="assets")