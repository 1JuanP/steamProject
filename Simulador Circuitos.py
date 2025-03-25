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

def add_component(e, components, component_type, component_value, connection_type_dropdown, result_text, page):
    try:
        value = float(component_value.value)
        connection = connection_type_dropdown.value.lower()
        component = {
            "type": component_type.value,
            "value": value,
            "connection": connection
        }
        components.append(component)
        result_text.value = f"Componente agregado: {component['type']} = {component['value']} ({connection.capitalize()})"
        page.update()
    except ValueError:
        result_text.value = "Error: Ingresa un valor numérico válido."
        page.update()

def calculate_circuit(e, components, result_text, page):
    if not components:
        result_text.value = "Error: No hay componentes en el circuito."
        page.update()
        return

    resistances_series = []
    resistances_parallel = []
    capacitances_series = []
    capacitances_parallel = []

    for component in components:
        if component["type"] == "Resistencia":
            if component["connection"] == "serie":
                resistances_series.append(component["value"])
            else:
                resistances_parallel.append(component["value"])
        elif component["type"] == "Capacitor":
            if component["connection"] == "serie":
                capacitances_series.append(component["value"])
            else:
                capacitances_parallel.append(component["value"])

    total_resistance = sum(resistances_series) + (1 / sum(1 / r for r in resistances_parallel) if resistances_parallel else 0)
    total_capacitance = sum(capacitances_parallel) + (1 / sum(1 / c for c in capacitances_series) if capacitances_series else 0)

    result = []
    if resistances_series or resistances_parallel:
        result.append(f"Resistencia equivalente: {total_resistance:.2f} Ohmios")
    if capacitances_series or capacitances_parallel:
        result.append(f"Capacitancia equivalente: {total_capacitance:.2f} Faradios")

    result_text.value = "\n".join(result)
    page.update()

def simulator_page(page: ft.Page):
    page.controls.clear()
    page.title = "Simulador de Circuitos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    components = []

    component_type = ft.Dropdown(
        options=[ft.dropdown.Option("Resistencia"), ft.dropdown.Option("Capacitor")],
        value="Resistencia",
        label="Tipo de componente"
    )
    component_value = ft.TextField(label="Valor", hint_text="Ejemplo: 100 (Ohmios/Faradios)")
    connection_type_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("Serie"), ft.dropdown.Option("Paralelo")],
        value="Serie",
        label="Conexión"
    )
    add_button = ft.ElevatedButton(
        "Agregar componente",
        on_click=lambda e: add_component(e, components, component_type, component_value, connection_type_dropdown, result_text, page)
    )
    calculate_button = ft.ElevatedButton(
        "Calcular",
        on_click=lambda e: calculate_circuit(e, components, result_text, page)
    )
    reset_button = ft.ElevatedButton("Resetear", on_click=lambda e: None)  # Placeholder
    result_text = ft.Text(style=ft.TextThemeStyle.HEADLINE_SMALL)
    circuit_diagram = ft.Column(spacing=10)

    legend = ft.Row(
        controls=[
            ft.Container(
                ft.Text("⚡ = Resistencia", size=12, color=ft.colors.WHITE),
                bgcolor=ft.colors.ORANGE,
                padding=5,
                border_radius=5,
                margin=ft.margin.only(right=10)
            ),
            ft.Container(
                ft.Text("⚡⚡ = Capacitor", size=12, color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN,
                padding=5,
                border_radius=5
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )

    main_content = ft.Column(
        controls=[
            ft.Container(circuit_diagram, padding=20, border=ft.border.all(2, ft.colors.BLACK), border_radius=10),
            legend,
            ft.Row([component_type, component_value, connection_type_dropdown, add_button]),
            ft.Row([calculate_button, reset_button]),
            result_text
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    page.add(main_content)

def main(page: ft.Page):
    page.title = "Simulador de Circuitos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    welcome_page(page)

ft.app(target=main, assets_dir="assets")