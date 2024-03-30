import flet as ft
import json
from flet import(
    Column,
    ListView,
    ButtonStyle,
    Container,
    ElevatedButton,
    Icon,
    icons,
    Text,
    Page,
    Row,
    RoundedRectangleBorder,
    MainAxisAlignment,
    CrossAxisAlignment,
    Margin,
    margin,
    TextAlign
)

import navigation
import services.config as sv_config
import services.servidor as sv_servidor

def main(page: ft.Page):

    page.appbar = ft.AppBar(
        leading = None,
        title=ft.Text("Produtos"),
        bgcolor=ft.colors.INDIGO,
    )

    def on_change_navbar(e):
        match e.control.selected_index:
            case 0:
                page.route = "/dispositivos"
                page.update()
            case 1:
                page.route = "/central"
                page.update()
            case 2:
                page.route = "/configuracoes"
                page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.PIE_CHART_OUTLINE_OUTLINED, selected_icon=ft.icons.PIE_CHART_OUTLINE, label="Dispositivos"),
            ft.NavigationDestination(icon=ft.icons.RECEIPT_LONG_OUTLINED, selected_icon=ft.icons.RECEIPT_LONG, label="Central"),
            #NavigationDestination(icon=ft.icons.SHOPPING_CART_OUTLINED, selected_icon=ft.icons.SHOPPING_CART, label="Produtos"),
            #NavigationDestination(icon=ft.icons.CATEGORY_OUTLINED, selected_icon=ft.icons.CATEGORY, label="Categorias"),
            ft.NavigationDestination(icon=ft.icons.ENGINEERING_OUTLINED, selected_icon=ft.icons.ENGINEERING, label="Configurações"),
        ],
        on_change = on_change_navbar,
        selected_index=1,
    )

    page.navigation_bar.visible = False
    page.appbar.visible = False

    main = Container()

    def route_change(e: ft.RouteChangeEvent):
        print(e.route)
        match e.route:
            case "/central":
                page.navigation_bar.visible = True
                page.appbar.visible = True
                listaDisp = []

                dispositivos = sv_servidor.dispositivos_usr()

                tela = Column(
                    [
                        ListView()
                    ],
                    #visible=False
                )

                for disp in dispositivos:
                    info = disp['info']
                    info_json = json.loads(info)
                    print(info_json)

                    listaDisp.append(
                        Container(
                            Row(
                                [
                                    Container(
                                        expand=True,
                                    ),
                                    ElevatedButton(
                                        content=Container(
                                            Row(
                                                [
                                                    Icon("add"),
                                                    Column(
                                                        [
                                                            Text(value=disp['nome'], size=20),
                                                            Text(value=disp['tipo']),
                                                        ],
                                                        spacing=5,
                                                    ),
                                                ],
                                                spacing=30
                                            ),
                                            margin=Margin(10,10,10,10)
                                        ),
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=10),
                                        ),
                                        height=150,
                                        width=150,
                                        key="Opa"
                                    ),
                                    Container(
                                        expand=True,
                                    ),
                                    ElevatedButton(
                                        content=Container(
                                            Row(
                                                [
                                                    #Icon("add"),
                                                    Column(
                                                        [
                                                            Container(
                                                                expand=True,
                                                            ),
                                                            Row(
                                                                [
                                                                    Icon("THERMOSTAT", size=30),
                                                                    Text(value=str(json.loads(disp['info'])['temp']) + " °C", size=20),
                                                                ],
                                                                spacing=30
                                                                #expand=True
                                                            ),
                                                            Container(
                                                                expand=True,
                                                            ),
                                                            Text(value="Temperatura do\nambiente", text_align=TextAlign.CENTER),
                                                            Container(
                                                                expand=True,
                                                            ),
                                                        ],
                                                        alignment=MainAxisAlignment.CENTER,
                                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                                        #spacing=5,
                                                    ),
                                                ],
                                                #spacing=30
                                            ),
                                            #margin=Margin(0,10,100,10)
                                        ),
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=10),
                                        ),
                                        #expand=True,
                                        height=150,
                                        width=150
                                    ),
                                    Container(
                                        expand=True,
                                    ),
                                ],
                                expand=True
                            )
                        )
                    )

                tela.controls = listaDisp
                main.content = tela
                page.update()

            case "/dispositivos":
                page.navigation_bar.visible = True
                page.appbar.visible = True

                listaDisp = []

                dispositivos = sv_servidor.dispositivos_usr()

                tela = Column(
                    [
                        ListView()
                    ],
                    #visible=False
                )

                for disp in dispositivos:
                    listaDisp.append(
                        Container(
                            ElevatedButton(
                                content=Container(
                                    Row(
                                        [
                                            Icon("add"),
                                            Column(
                                                [
                                                    Text(value=disp['nome'], size=20),
                                                    Text(value=disp['tipo']),
                                                ],
                                                alignment=MainAxisAlignment.CENTER,
                                                spacing=5,
                                            ),
                                        ],
                                        spacing=30
                                    ),
                                    margin=Margin(10,10,10,10)
                                ),
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                            )
                        )
                    )

                tela.controls = listaDisp
                main.content = tela
                page.update()

    page.on_route_change = route_change
    page.add(main)

ft.app(target=main, view=ft.WEB_BROWSER)