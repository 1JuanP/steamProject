import flet as ft

def welcome_page(page: ft.Page):
    page.title = "Simulador de Circuitos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.with_opacity(0.9, "#E0F7FA")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    logo = ft.Image(src="circuit_logo.png", width=150, height=150, fit=ft.ImageFit.CONTAIN)
    title = ft.Text("Bienvenido al Simulador de Circuitos", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_900, text_align=ft.TextAlign.CENTER)
    description = ft.Text(
        "Explora y simula circuitos eléctricos añadiendo resistencias y capacitores en serie o paralelo. Calcula valores equivalentes fácilmente.",
        size=16, color=ft.colors.GREY_800, text_align=ft.TextAlign.CENTER, width=500
    )
    image1 = ft.Image(src="image1.jpg", width=200, height=100, fit=ft.ImageFit.CONTAIN)
    image2 = ft.Image(src="image2.jpg", width=200, height=100, fit=ft.ImageFit.CONTAIN)
    instructions = ft.Text("Haz clic en 'Iniciar Simulador' para comenzar.", size=14, color=ft.colors.GREY_600, text_align=ft.TextAlign.CENTER)
    
    start_button = ft.ElevatedButton(
        "Iniciar Simulador",
        on_click=lambda e: (page.clean(), simulator_page(page)),
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15,
            elevation=5
        ),
        width=200
    )
    
    content = ft.Container(
        content=ft.Column(
            controls=[
                logo,
                title,
                description,
                ft.Row([image1, image2], alignment=ft.MainAxisAlignment.CENTER),
                instructions,
                start_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        ),
        padding=30,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.colors.GREY_400, offset=ft.Offset(0, 5)),
        width=700,
        alignment=ft.alignment.center
    )
    page.add(content)

def info_page(page: ft.Page):
    def back_to_simulator(e):
        page.clean()
        simulator_page(page)
    
    page.title = "Información de Fórmulas"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    content = ft.Column([
        ft.Text("Fórmulas de Cálculo", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("Resistencias en serie: R_eq = R1 + R2 + ... + Rn", size=16),
        ft.Text("Resistencias en paralelo: 1/R_eq = 1/R1 + 1/R2 + ...", size=16),
        ft.Text("Capacitores en serie: 1/C_eq = 1/C1 + 1/C2 + ...", size=16),
        ft.Text("Capacitores en paralelo: C_eq = C1 + C2 + ...", size=16),
        ft.ElevatedButton("Volver al Simulador", on_click=back_to_simulator)
    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20)
    
    page.add(
        ft.Container(
            content=content,
            padding=50,
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=15)
        )
    )

def simulator_page(page: ft.Page):
    components = []
    
    def add_component(e):
        try:
            value = float(component_value.value)
            if value == 0:
                result_text.value = "Error: El valor no puede ser 0."
                page.update()
                return
            connection = connection_type_dropdown.value.lower()
            component = {"type": component_type.value, "value": value, "connection": connection}
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
        
        resistances_series, resistances_parallel = [], []
        capacitances_series, capacitances_parallel = [], []
        
        for component in components:
            if component["type"] == "Resistencia":
                if component["connection"] == "serie": resistances_series.append(component["value"])
                else: resistances_parallel.append(component["value"])
            elif component["type"] == "Capacitor":
                if component["connection"] == "serie": capacitances_series.append(component["value"])
                else: capacitances_parallel.append(component["value"])
        
        total_resistance = sum(resistances_series) + (1 / sum(1/r for r in resistances_parallel) if resistances_parallel else 0)
        total_capacitance = sum(capacitances_parallel) + (1 / sum(1/c for c in capacitances_series) if capacitances_series else 0)
        
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
        update_circuit_diagram()
        result_text.value = "Circuito reseteado."
        page.update()
    
    def update_circuit_diagram():
        circuit_diagram.controls.clear()
        circuit_diagram.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("Batería", size=12, color=ft.colors.WHITE),
                        bgcolor=ft.colors.BLUE_600,
                        padding=10,
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_400)
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
                        icon = "Ω" if pc["type"] == "Resistencia" else "C"
                        color = ft.colors.ORANGE_600 if pc["type"] == "Resistencia" else ft.colors.GREEN_600
                        component_container = ft.Container(
                            content=ft.Text(f"{icon} {pc['value']}", size=14, color=ft.colors.WHITE),
                            bgcolor=color,
                            padding=10,
                            border_radius=10,
                            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_400)
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
                
                icon = "Ω" if component["type"] == "Resistencia" else "C"
                color = ft.colors.ORANGE_600 if component["type"] == "Resistencia" else ft.colors.GREEN_600
                main_row.controls.append(
                    ft.Container(
                        content=ft.Text(f"{icon} {component['value']}", size=14, color=ft.colors.WHITE),
                        bgcolor=color,
                        padding=10,
                        border_radius=10,
                        shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_400)
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
                icon = "Ω" if pc["type"] == "Resistencia" else "C"
                color = ft.colors.ORANGE_600 if pc["type"] == "Resistencia" else ft.colors.GREEN_600
                component_container = ft.Container(
                    content=ft.Text(f"{icon} {pc['value']}", size=14, color=ft.colors.WHITE),
                    bgcolor=color,
                    padding=10,
                    border_radius=10,
                    shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_400)
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
        
        circuit_diagram.controls.append(main_row)
        circuit_diagram.controls.append(ft.Container(height=2, bgcolor=ft.colors.BLACK))
        
        photos_row = ft.Row(
            controls=[
                ft.Image(src="resistor.jpg", width=100, height=100, fit=ft.ImageFit.CONTAIN),
                ft.Image(src="capacitor.jpg", width=100, height=100, fit=ft.ImageFit.CONTAIN),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        circuit_diagram.controls.append(photos_row)
        page.update()
    
    page.title = "Simulador de Circuitos"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.GREY_100
    
    def help_button_click(e):
        page.clean()
        info_page(page)
    
    help_button = ft.IconButton(
        icon=ft.icons.HELP_OUTLINE,
        icon_color=ft.colors.BLUE_600,
        tooltip="Ayuda sobre fórmulas",
        on_click=help_button_click
    )
    
    top_bar = ft.Row(
        controls=[
            ft.Container(expand=True),
            help_button
        ],
        alignment=ft.MainAxisAlignment.END
    )
    
    component_type = ft.Dropdown(
        options=[ft.dropdown.Option("Resistencia"), ft.dropdown.Option("Capacitor")],
        value="Resistencia",
        label="Tipo de componente",
        bgcolor=ft.colors.WHITE,
        border_radius=5
    )
    
    component_value = ft.TextField(
        label="Valor",
        hint_text="Ejemplo: 100 (Ohmios/Faradios)",
        bgcolor=ft.colors.WHITE,
        border_radius=5
    )
    
    connection_type_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("Serie"), ft.dropdown.Option("Paralelo")],
        value="Serie",
        label="Conexión",
        bgcolor=ft.colors.WHITE,
        border_radius=5
    )
    
    add_button = ft.ElevatedButton(
        "Agregar componente",
        on_click=add_component,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        )
    )
    
    calculate_button = ft.ElevatedButton(
        "Calcular",
        on_click=calculate_circuit,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        )
    )
    
    reset_button = ft.ElevatedButton(
        "Resetear",
        on_click=reset_circuit,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.RED_600,
            color=ft.colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=15
        )
    )
    
    result_text = ft.Text(style=ft.TextThemeStyle.HEADLINE_SMALL, color=ft.colors.BLUE_900)
    circuit_diagram = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
    
    legend = ft.Row(
        controls=[
            ft.Container(
                ft.Text("Ω = Resistencia", size=12, color=ft.colors.WHITE),
                bgcolor=ft.colors.ORANGE_600,
                padding=10,
                border_radius=10,
                margin=ft.margin.only(right=10)
            ),
            ft.Container(
                ft.Text("C = Capacitor", size=12, color=ft.colors.WHITE),
                bgcolor=ft.colors.GREEN_600,
                padding=10,
                border_radius=10
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                component_type,
                component_value,
                connection_type_dropdown,
                add_button,
                calculate_button,
                reset_button,
                legend
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START
        ),
        padding=20,
        bgcolor=ft.colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.GREY_400),
        width=300
    )
    
    main_content = ft.Column(
        controls=[
            top_bar,
            ft.Row(
                controls=[
                    sidebar,
                    ft.Container(
                        content=circuit_diagram,
                        padding=20,
                        border=ft.border.all(2, ft.colors.BLACK),
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        expand=True,
                        height=400
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
    
    page.add(main_content, result_text)

def main(page: ft.Page):
    welcome_page(page)

ft.app(target=main, assets_dir="assets")