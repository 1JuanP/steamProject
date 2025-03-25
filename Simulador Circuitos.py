import flet as ft

def simulator_page(page: ft.Page):
    page.title = "Simulador de Circuitos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    components = []

    def add_component(e):
        try:
            value = float(component_value.value)
            connection = connection_type_dropdown.value.lower()
            component = {
                "type": component_type.value,
                "value": value,
                "connection": connection
            }
            components.append(component)
            update_circuit_diagram()
            result_text.value = f"Componente agregado: {component['type']} = {component['value']} ({connection.capitalize()})"
            page.update()
        except ValueError:
            result_text.value = "Error: Ingresa un valor numérico válido."
            page.update()

    def calculate_circuit(e):
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

    def reset_circuit(e):
        nonlocal components
        components = []
        circuit_diagram.controls = []
        result_text.value = "Circuito reseteado."
        page.update()

    def update_circuit_diagram():
        circuit_diagram.controls.clear()

        circuit_diagram.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("Batería", size=12, color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE,
                        padding=5,
                        border_radius=5,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        )

        circuit_diagram.controls.append(ft.Container(height=2, bgcolor=ft.colors.BLACK))

        main_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=20, scroll=ft.ScrollMode.AUTO)
        current_parallel_components = []

        for component in components:
            if component["connection"] == "serie":
                if current_parallel_components:
                    n_parallel = len(current_parallel_components)
                    vertical_height = n_parallel * 50

                    left_vertical = ft.Container(width=2, height=vertical_height, bgcolor=ft.colors.BLACK)
                    right_vertical = ft.Container(width=2, height=vertical_height, bgcolor=ft.colors.BLACK)

                    parallel_column = ft.Column(spacing=10)
                    for pc in current_parallel_components:
                        icon = "⚡" if pc["type"] == "Resistencia" else "⚡⚡"
                        color = ft.colors.ORANGE if pc["type"] == "Resistencia" else ft.colors.GREEN
                        component_container = ft.Container(
                            content=ft.Text(f"{icon} {pc['value']}", size=14, color=ft.colors.WHITE),
                            bgcolor=color,
                            padding=5,
                            border_radius=5
                        )
                        parallel_row = ft.Row(
                            [
                                ft.Container(width=20, height=2, bgcolor=ft.colors.BLACK),
                                component_container,
                                ft.Container(width=20, height=2, bgcolor=ft.colors.BLACK)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                        parallel_column.controls.append(parallel_row)

                    parallel_group = ft.Row(
                        [
                            left_vertical,
                            parallel_column,
                            right_vertical
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )

                    main_row.controls.append(parallel_group)
                    main_row.controls.append(ft.Container(width=20, height=2, bgcolor=ft.colors.BLACK))
                    current_parallel_components = []

                icon = "⚡" if component["type"] == "Resistencia" else "⚡⚡"
                color = ft.colors.ORANGE if component["type"] == "Resistencia" else ft.colors.GREEN
                main_row.controls.append(
                    ft.Container(
                        content=ft.Text(f"{icon} {component['value']}", size=14, color=ft.colors.WHITE),
                        bgcolor=color,
                        padding=5,
                        border_radius=5
                    )
                )
                main_row.controls.append(ft.Container(width=20, height=2, bgcolor=ft.colors.BLACK))
            else:
                current_parallel_components.append(component)

        if current_parallel_components:
            n_parallel = len(current_parallel_components)
            vertical_height = n_parallel * 50

            left_vertical = ft.Container(width=2, height=vertical_height, bgcolor=ft.colors.BLACK)
            right_vertical = ft.Container(width=2, height=vertical_height, bgcolor=ft.colors.BLACK)

            parallel_column = ft.Column(spacing=10)
            for pc in current_parallel_components:
                icon = "⚡" if pc["type"] == "Resistencia" else "⚡⚡"
                color = ft.colors.ORANGE if pc["type"] == "Resistencia" else ft.colors.GREEN
                component_container = ft.Container(
                    content=ft.Text(f"{icon} {pc['value']}", size=14, color=ft.colors.WHITE),
                    bgcolor=color,
                    padding=5,
                    border_radius=5
                )
                parallel_row = ft.Row(
                    [
                        ft.Container(width=20, height=2, bgcolor=ft.colors.BLACK),
                        component_container,
                        ft.Container(width=20, height=2, bgcolor=ft.colors.BLACK)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                )
                parallel_column.controls.append(parallel_row)

            parallel_group = ft.Row(
                [
                    left_vertical,
                    parallel_column,
                    right_vertical
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )

            main_row.controls.append(parallel_group)
            main_row.controls.append(ft.Container(width=20, height=2, bgcolor=ft.colors.BLACK))

        circuit_diagram.controls.append(main_row)

        circuit_diagram.controls.append(ft.Container(height=2, bgcolor=ft.colors.BLACK))

        page.update()

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
    add_button = ft.ElevatedButton("Agregar componente", on_click=add_component)
    calculate_button = ft.ElevatedButton("Calcular", on_click=calculate_circuit)
    reset_button = ft.ElevatedButton("Resetear", on_click=reset_circuit)
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







