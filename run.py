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
    TextAlign,
    Image,
    ImageFit,
    ImageRepeat,
    border_radius,
    Padding,
    TextButton,
)

import navigation
import services.config as sv_config
import services.servidor as sv_servidor

def main(page: ft.Page):

    page.session.set("token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9wdWJsaWNvIjoiYTcwMDM4YzQtZGU0Mi00NmY4LWIxY2EtMzQwN2FhMDhkM2U5In0.YIAKhE7lWZUvzJsI_-mGAzMTvdpyOKs7v_X398WSOuE")

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
    page.appbar = ft.AppBar(leading=None, title=ft.Text("Aplicativo"), bgcolor=ft.colors.INDIGO)

    main = Container(expand=True)

    def back(e):
        rotas = str(page.route).split("/")
        #join rotas com /
        join_rotas = "/".join(rotas[:-1])
        page.route = join_rotas
        page.update()

    def sair(e):
        page.session.set("token", "aaa")
        page.route = "/login"
        page.update()

    def verify_token():
        token = page.session.get("token")
        if token == "aaa":
            page.route = "/login"
            page.update()
            return False
        else:
            if sv_servidor.verificar_token(token):
                return True
            else:
                page.route = "/login"
                page.update()
                return False

    def route_change(e: ft.RouteChangeEvent):
        match e.route:
            case "/":
                if verify_token():
                    page.route = "/central"
                    page.update()

            case "/login":
                page.navigation_bar.visible = False
                page.appbar.visible = False
                #page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Residencias"), bgcolor=ft.colors.INDIGO)

                tela = Container(

                )

                #tela.controls = nova_tela
                main.content = tela
                page.update()

            case "/central":
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=None, title=ft.Text("Central"), bgcolor=ft.colors.INDIGO)
                    page.floating_action_button = None
                    listaDisp = []

                    dispositivos = sv_servidor.dispositivos_usr()

                    tela = Column(
                        [
                            ListView()
                        ],
                        #visible=False
                    )

                    for disp in dispositivos:

                        print(json.loads(disp['info'])['temp'])

                        sensor_info = {
                            "termometro": {
                                "icon": "THERMOSTAT",
                                "label": "Temperatura do\nambiente",
                                "value": str(json.loads(disp['info'])['temp']) + " °C"
                            },
                            "gas": {
                                "icon": "GAS_STATION",
                                "label": "Gás",
                                "value": str(disp['data_alteracao'])
                            },
                            "presenca": {
                                "icon": "PEOPLE",
                                "label": "Presença",
                                "value": str(disp['data_alteracao'])
                            },
                        }

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
                                                        #Icon("add"),
                                                        Column(
                                                            [
                                                                Container(
                                                                    expand=True,
                                                                ),
                                                                Row(
                                                                    [
                                                                        Icon(sensor_info[disp['tipo']]['icon'], size=30),
                                                                        Text(value=sensor_info[disp['tipo']]['value'], size=20),
                                                                    ],
                                                                    spacing=30
                                                                    #expand=True
                                                                ),
                                                                Container(
                                                                    expand=True,
                                                                ),
                                                                Text(value=sensor_info[disp['tipo']]['label'], text_align=TextAlign.CENTER),
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
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=None, title=ft.Text("Dispositivos"), bgcolor=ft.colors.INDIGO)

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
                    page.floating_action_button = ft.FloatingActionButton(
                        icon=ft.icons.ADD,
                        #on_click=fab_pressed,
                        #bgcolor=ft.colors.LIME_300
                    )
                    page.update()

            case "/configuracoes":
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=None, title=ft.Text("Configurações"), bgcolor=ft.colors.INDIGO)
                    page.floating_action_button = None

                    def go_to_residencias(e):
                        page.route = "/configuracoes/residencias"
                        page.update()

                    tela = Column(
                        [
                            ListView()
                        ],
                        expand=True
                    )

                    nova_tela = [
                        Container(
                            Column(
                                [
                                    Row(
                                        [
                                            Image(
                                                src="/images/perfil.jpg",
                                                width=150,
                                                height=150,
                                                fit=ImageFit.NONE,
                                                repeat=ImageRepeat.NO_REPEAT,
                                                border_radius=border_radius.all(100)
                                            ),
                                        ],
                                        #expand=True,
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    Column(
                                        [
                                            Container(
                                                Row(
                                                    [
                                                        TextButton(
                                                            expand=True,
                                                            content=Container(
                                                                Row(
                                                                    [
                                                                        Icon(icons.PERSON_2_ROUNDED, size=30),
                                                                        Text("Seus dados", size=20),
                                                                    ],
                                                                    alignment=MainAxisAlignment.START,
                                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                                )
                                                            ),
                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.START,
                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                            ),
                                            Container(
                                                Row(
                                                    [
                                                        TextButton(
                                                            expand=True,
                                                            content=Container(
                                                                Row(
                                                                    [
                                                                        Icon(icons.HOME_ROUNDED, size=30),
                                                                        Text("Residencias", size=20),
                                                                    ],
                                                                    alignment=MainAxisAlignment.START,
                                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                                )
                                                            ),
                                                            on_click=go_to_residencias,
                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.START,
                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                            ),
                                            Container(
                                                Row(
                                                    [
                                                        TextButton(
                                                            expand=True,
                                                            content=Container(
                                                                Row(
                                                                    [
                                                                        Icon(icons.LOGOUT_ROUNDED, size=30),
                                                                        Text("Sair", size=20),
                                                                    ],
                                                                    alignment=MainAxisAlignment.START,
                                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                                )
                                                            ),
                                                            on_click=sair,
                                                        ),
                                                    ],
                                                    alignment=MainAxisAlignment.START,
                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                            ),
                                        ],
                                        expand=True,
                                    )
                                ]
                            ),
                            margin=margin.only(top=50),
                        )
                    ]

                    tela.controls = nova_tela
                    main.content = tela
                    page.update()

            case "/configuracoes/residencias":
                if verify_token():
                    page.navigation_bar.visible = False
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Residencias"), bgcolor=ft.colors.INDIGO)

                    residencias = sv_servidor.residencias_usr(page.session.get("token"))

                    tela = Container(
                        Column(
                            [
                                ListView()
                            ],
                            #visible=False
                        )
                    )

                    listaResids = []

                    for resid in residencias:
                        listaResids.append(
                            Container(
                                ElevatedButton(
                                    content=Container(
                                        Row(
                                            [
                                                Icon("home"),
                                                Column(
                                                    [
                                                        Text(value=resid['nome'], size=20),
                                                        Text(value=resid['id']),
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

                    tela.content.controls = listaResids

                    #tela.controls = nova_tela
                    main.content = tela
                    page.update()

    page.route = "/central"
    page.update()

    page.on_route_change = route_change
    page.add(main)

ft.app(
    target=main,
    host="0.0.0.0",
    port=22022,
    assets_dir="assets",
    view=ft.WEB_BROWSER
)