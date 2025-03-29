import flet as ft

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

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(create_home_page())
        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)