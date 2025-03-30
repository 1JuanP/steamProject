import flet as ft
import math

def main(page: ft.Page):
    page.title = "Simulador de Campo Magnético"
    page.window_width = 800
    page.window_height = 600
    page.window_min_width = 800
    page.window_min_height = 600

    page.bgcolor = ft.colors.BLACK
    page.gradient = ft.LinearGradient(
        begin=ft.alignment.top_left,
        end=ft.alignment.bottom_right,
        colors=[ft.colors.BLACK, ft.colors.BLUE_900]
    )

    def on_resize(e):
        page.update()

    page.on_resize = on_resize

    def create_home_page():
        title = ft.Text(
            "Campo Magnético",
            size=50,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.WHITE,
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.BLUE_200))
        )
        description = ft.Text(
            "Un campo magnético es una región del espacio donde se manifiestan fuerzas magnéticas. "
            "Es generado por imanes, corrientes eléctricas o cambios en campos eléctricos. "
            "Los campos magnéticos son fundamentales en la física y tienen aplicaciones en motores eléctricos, "
            "generadores, resonancia magnética (MRI) y tecnologías de almacenamiento de datos como discos duros. "
            "En este simulador, podrás explorar cómo un dipolo magnético o corriente afecta las líneas de campo magnético y ajustar su intensidad.",
            size=20,
            color=ft.colors.WHITE,
            text_align=ft.TextAlign.CENTER,
            width=600
        )
        facts = ft.Column(
            [
                ft.Text("• Los campos magnéticos son vectoriales y se miden en teslas (T).", color=ft.colors.WHITE, size=16),
                ft.Text("• Las líneas de campo van del polo norte al polo sur de un imán.", color=ft.colors.WHITE, size=16),
                ft.Text("• La Tierra tiene su propio campo magnético, que protege contra el viento solar.", color=ft.colors.WHITE, size=16),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        button = ft.ElevatedButton(
            "Ir al simulador",
            on_click=lambda e: page.go("/simulator"),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE,
                padding=15,
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=5,
                overlay_color=ft.colors.BLUE_500
            )
        )
        home_content = ft.Column(
            [title, description, facts, button],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30,
            expand=True
        )
        centered_content = ft.Container(
            content=home_content,
            alignment=ft.alignment.center,
            expand=True
        )
        return ft.View("/", [centered_content], bgcolor=ft.colors.TRANSPARENT)

    def create_simulator_page():
        main_stack = ft.Stack(expand=True)

        marco_width = 600
        marco_height = 400

        marco = ft.Container(
            width=marco_width,
            height=marco_height,
            border=ft.Border(
                top=ft.BorderSide(4, ft.colors.WHITE),
                bottom=ft.BorderSide(4, ft.colors.WHITE),
                left=ft.BorderSide(4, ft.colors.WHITE),
                right=ft.BorderSide(4, ft.colors.WHITE)
            ),
            bgcolor=ft.colors.BLACK,
            alignment=ft.alignment.center,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.colors.BLUE_200)
        )

        stack = ft.Stack(width=marco_width, height=marco_height)

        grid_size = 8
        arrow_spacing = marco_width / (grid_size + 1)
        arrows = []
        for i in range(grid_size):
            for j in range(grid_size):
                x = (i + 1) * arrow_spacing
                y = (j + 1) * arrow_spacing
                arrow = ft.Icon(
                    ft.icons.ARROW_UPWARD,
                    size=20,
                    color=ft.colors.YELLOW,
                    rotate=0,
                    opacity=1.0
                )
                arrow_container = ft.Container(arrow, left=x, top=y)
                arrows.append(arrow_container)
                stack.controls.append(arrow_container)

        carga_size = 30
        carga_color = ft.colors.RED
        carga = ft.Container(
            width=carga_size,
            height=carga_size,
            bgcolor=carga_color,
            border_radius=carga_size / 2,
            shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.WHITE)
        )
        carga_container = ft.Container(content=carga)

        dragging = False
        last_x = 0
        last_y = 0

        carga_sign = 1

        def set_positive(e):
            nonlocal carga_sign, carga_color
            carga_sign = 1
            carga_color = ft.colors.RED
            carga.bgcolor = carga_color
            page.update()

        def set_negative(e):
            nonlocal carga_sign, carga_color
            carga_sign = -1
            carga_color = ft.colors.BLUE
            carga.bgcolor = carga_color
            page.update()

        positive_button = ft.ElevatedButton(
            "Polo Norte",
            on_click=set_positive,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED_700,
                color=ft.colors.WHITE,
                elevation=5,
                overlay_color=ft.colors.RED_500
            )
        )
        negative_button = ft.ElevatedButton(
            "Polo Sur",
            on_click=set_negative,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE,
                elevation=5,
                overlay_color=ft.colors.BLUE_500
            )
        )
        buttons_row = ft.Row(
            [positive_button, negative_button],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )

        def on_pan_start(e: ft.DragStartEvent):
            nonlocal dragging, last_x, last_y
            dragging = True
            last_x = e.global_x
            last_y = e.global_y

        def on_pan_update(e: ft.DragUpdateEvent):
            nonlocal last_x, last_y
            if dragging:
                delta_x = e.global_x - last_x
                delta_y = e.global_y - last_y
                carga_gesture.left = (carga_gesture.left or 0) + delta_x
                carga_gesture.top = (carga_gesture.top or 0) + delta_y
                last_x = e.global_x
                last_y = e.global_y
                page.update()

        def on_pan_end(e: ft.DragEndEvent):
            nonlocal dragging
            dragging = False

        carga_gesture = ft.GestureDetector(
            content=carga_container,
            left=marco_width / 2 - carga_size / 2,
            top=marco_height / 2 - carga_size / 2,
            on_pan_start=on_pan_start,
            on_pan_update=on_pan_update,
            on_pan_end=on_pan_end
        )
        stack.controls.append(carga_gesture)

        marco.content = stack

        back_button = ft.ElevatedButton(
            "Volver a Inicio",
            on_click=lambda e: page.go("/"),
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_700,
                color=ft.colors.WHITE,
                padding=10,
                shape=ft.RoundedRectangleBorder(radius=10),
                elevation=5,
                overlay_color=ft.colors.BLUE_500
            )
        )

        intensity_label = ft.Text("Intensidad del Campo: 100%", color=ft.colors.WHITE, size=16)
        intensity_slider = ft.Slider(
            min=0,
            max=100,
            value=100,
            divisions=100,
            label="{value}%",
            width=300,
            active_color=ft.colors.BLUE_500,
            inactive_color=ft.colors.GREY_700,
            thumb_color=ft.colors.WHITE
        )

        def update_intensity(e):
            intensity = intensity_slider.value
            intensity_label.value = f"Intensidad del Campo: {int(intensity)}%"
            for arrow_container in arrows:
                arrow_container.content.opacity = intensity / 100
            page.update()

        intensity_slider.on_change = update_intensity

        simulator_content = ft.Column(
            [
                ft.Container(height=20),
                back_button,
                ft.Container(height=20),
                marco,
                ft.Container(height=20),
                buttons_row,
                ft.Container(height=20),
                intensity_label,
                intensity_slider
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )

        centered_content = ft.Container(
            content=simulator_content,
            alignment=ft.alignment.center,
            expand=True
        )

        main_stack.controls.append(centered_content)

        return ft.View("/simulator", [main_stack], bgcolor=ft.colors.TRANSPARENT)

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(create_home_page())
        elif page.route == "/simulator":
            page.views.append(create_simulator_page())
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)