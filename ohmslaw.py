import random
import flet as ft

def principal(pagina: ft.Page):
    pagina.title = "Resolvedor de Física de la Ley de Ohm"
    pagina.theme_mode = ft.ThemeMode.DARK
    pagina.bgcolor = "#1A1A2E"
    pagina.padding = 20
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def generar_problema_ley_de_ohm(dificultad):
        if dificultad == 'Fácil':
            V = random.randint(1, 20)
            R = random.randint(1, 20)
            I = round(V / R, 2)
            variable_a_resolver = random.choice(['V', 'I', 'R'])
            if variable_a_resolver == 'V':
                problema = f"Un circuito tiene una corriente de {I} A y una resistencia de {R} Ω. ¿Cuál es el voltaje?"
                respuesta = V
            elif variable_a_resolver == 'I':
                problema = f"Un circuito tiene un voltaje de {V} V y una resistencia de {R} Ω. ¿Cuál es la corriente?"
                respuesta = I
            else:
                problema = f"Un circuito tiene un voltaje de {V} V y una corriente de {I} A. ¿Cuál es la resistencia?"
                respuesta = R
        elif dificultad == 'Medio':
            R1 = random.randint(1, 10)
            R2 = random.randint(1, 10)
            V = random.randint(10, 50)
            combinacion = random.choice(['serie', 'paralelo'])
            if combinacion == 'serie':
                Req = R1 + R2
                problema = f"Dos resistencias, R1 = {R1} Ω y R2 = {R2} Ω, están en serie. El voltaje es {V} V. Encuentra la corriente."
                respuesta = round(V / Req, 2)
            else:
                Req = round((R1 * R2) / (R1 + R2), 2)
                problema = f"Dos resistencias, R1 = {R1} Ω y R2 = {R2} Ω, están en paralelo. El voltaje es {V} V. Encuentra la corriente."
                respuesta = round(V / Req, 2)
        elif dificultad == 'Difícil':
            V = random.randint(20, 100)
            R = random.randint(10, 50)
            problema = f"Un circuito tiene {V} V y {R} Ω. ¿Cuál es la potencia disipada?"
            respuesta = round((V ** 2) / R, 2)
        return {"problema": problema, "respuesta": respuesta}

    def al_cambiar_dificultad(e):
        dificultad = selector_dificultad.value
        datos_problema = generar_problema_ley_de_ohm(dificultad)
        texto_problema.value = datos_problema["problema"]
        respuesta_correcta.value = str(datos_problema["respuesta"])
        campo_respuesta_usuario.value = ""
        texto_retroalimentacion.value = ""

        if dificultad == "Fácil":
            indicador_dificultad.content = ft.Icon(ft.icons.CIRCLE, color="#00C853")
        elif dificultad == "Medio":
            indicador_dificultad.content = ft.Icon(ft.icons.CIRCLE, color="#FFD600")
        elif dificultad == "Difícil":
            indicador_dificultad.content = ft.Icon(ft.icons.CIRCLE, color="#D50000")

        pagina.update()

    def verificar_respuesta(e):
        try:
            respuesta_usuario = float(campo_respuesta_usuario.value)
            correcta = float(respuesta_correcta.value)
            if abs(respuesta_usuario - correcta) < 0.06:
                texto_retroalimentacion.value = "¡Correcto! ¡Buen trabajo! ⚡"
                texto_retroalimentacion.color = "#00E676"
            else:
                texto_retroalimentacion.value = f"Incorrecto. Respuesta correcta: {respuesta_correcta.value}"
                texto_retroalimentacion.color = "#FF1744"
        except ValueError:
            texto_retroalimentacion.value = "¡Ingresa un número válido!"
            texto_retroalimentacion.color = "#FF1744"
        pagina.update()

    def resolver_ley_de_ohm(e):
        try:
            V = float(entrada_voltaje.value) if entrada_voltaje.value else None
            I = float(entrada_corriente.value) if entrada_corriente.value else None
            R1 = float(entrada_r1.value) if entrada_r1.value else None
            R2 = float(entrada_r2.value) if entrada_r2.value else None
            combinacion = selector_combinacion.value
            if R1 is not None and R2 is not None:
                Req = R1 + R2 if combinacion == "serie" else round((R1 * R2) / (R1 + R2), 2)
                if V is not None:
                    I = V / Req
                    P = V * I
                elif I is not None:
                    V = I * Req
                    P = I ** 2 * Req
                else:
                    V, I, P = None, None, None
            elif V is not None and I is not None:
                Req = V / I
                P = V * I
            else:
                V, I, Req, P = None, None, None, None
            resultado_voltaje.value = f"{V:.2f} V" if V else "N/A"
            resultado_corriente.value = f"{I:.2f} A" if I else "N/A"
            resultado_resistencia.value = f"{Req:.2f} Ω" if Req else "N/A"
            resultado_potencia.value = f"{P:.2f} W" if P else "N/A"
            pagina.update()
        except ValueError:
            resultado_voltaje.value = "Inválido"
            resultado_corriente.value = "Inválido"
            resultado_resistencia.value = "Inválido"
            resultado_potencia.value = "Inválido"
            pagina.update()

    selector_dificultad = ft.Dropdown(
        options=[ft.dropdown.Option(clave) for clave in ["Fácil", "Medio", "Difícil"]],
        value="Fácil",
        on_change=al_cambiar_dificultad,
        width=200,
        bgcolor="#16213E",
        border_radius=10,
        color="#E0E0E0",
    )

    indicador_dificultad = ft.Container(
        content=ft.Icon(ft.icons.CIRCLE, color="#00C853"),
        alignment=ft.alignment.center_right,
        padding=5,
    )

    texto_problema = ft.Text(size=16, weight=ft.FontWeight.BOLD, color="#E0E0E0", text_align=ft.TextAlign.CENTER)
    campo_respuesta_usuario = ft.TextField(
        label="Tu Respuesta",
        width=200,
        bgcolor="#16213E",
        border_radius=10,
        color="#E0E0E0",
        border_color="#0F3460",
    )

    boton_enviar = ft.ElevatedButton(
        "Enviar",
        on_click=verificar_respuesta,
        bgcolor="#0F3460",
        color="#E0E0E0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    texto_retroalimentacion = ft.Text(size=14, italic=True)
    respuesta_correcta = ft.Text(visible=False)

    problema_inicial = generar_problema_ley_de_ohm("Fácil")
    texto_problema.value = problema_inicial["problema"]
    respuesta_correcta.value = str(problema_inicial["respuesta"])

    entrada_voltaje = ft.TextField(label="Voltaje (V)", width=150, bgcolor="#16213E", border_radius=5, color="#E0E0E0")
    entrada_corriente = ft.TextField(label="Corriente (I)", width=150, bgcolor="#16213E", border_radius=5, color="#E0E0E0")
    entrada_r1 = ft.TextField(label="R1 (Ω)", width=150, bgcolor="#16213E", border_radius=5, color="#E0E0E0")
    entrada_r2 = ft.TextField(label="R2 (Ω)", width=150, bgcolor="#16213E", border_radius=5, color="#E0E0E0")

    selector_combinacion = ft.Dropdown(
        label="Tipo de Circuito",
        options=[ft.dropdown.Option(clave) for clave in ["serie", "paralelo"]],
        value="serie",
        width=150,
        bgcolor="#16213E",
        border_radius=5,
        color="#E0E0E0",
    )
    boton_calcular = ft.ElevatedButton(
        "Calcular",
        on_click=resolver_ley_de_ohm,
        bgcolor="#0F3460",
        color="#E0E0E0",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
    )

    resultado_voltaje = ft.Text(size=14, color="#BB86FC")
    resultado_corriente = ft.Text(size=14, color="#BB86FC")
    resultado_resistencia = ft.Text(size=14, color="#BB86FC")
    resultado_potencia = ft.Text(size=14, color="#BB86FC")

    pagina.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text("Problema de Física", size=20, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
                                    indicador_dificultad,
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            selector_dificultad,
                            ft.Container(
                                content=texto_problema,
                                padding=10,
                                bgcolor="#16213E",
                                border_radius=10,
                            ),
                            campo_respuesta_usuario,
                            boton_enviar,
                            texto_retroalimentacion,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=15,
                    ),
                    padding=20,
                    bgcolor="#0F3460",
                    border_radius=15,
                    width=400,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=["#0F3460", "#16213E"],
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Resolvedor de la Ley de Ohm", size=20, weight=ft.FontWeight.BOLD, color="#E0E0E0"),
                            entrada_voltaje,
                            entrada_corriente,
                            entrada_r1,
                            entrada_r2,
                            selector_combinacion,
                            boton_calcular,
                            ft.Row([ft.Text("V:", color="#E0E0E0"), resultado_voltaje], spacing=5),
                            ft.Row([ft.Text("I:", color="#E0E0E0"), resultado_corriente], spacing=5),
                            ft.Row([ft.Text("R:", color="#E0E0E0"), resultado_resistencia], spacing=5),
                            ft.Row([ft.Text("P:", color="#E0E0E0"), resultado_potencia], spacing=5),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=15,
                    ),
                    padding=20,
                    bgcolor="#0F3460",
                    border_radius=15,
                    width=300,
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(-1, -1),
                        end=ft.Alignment(1, 1),
                        colors=["#0F3460", "#16213E"],
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=20,
        )
    )

ft.app(target=principal)