from datetime import datetime
from time import sleep
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

    main = Column(expand=True)

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
                main.controls = [tela]
                page.update()

            case "/central":
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=None, title=ft.Text("Central"), bgcolor=ft.colors.INDIGO)
                    page.floating_action_button = None
                    listaDisp = []

                    disp_flet = []

                    dispositivos = sv_servidor.dispositivos_usr()

                    for disp in dispositivos:

                        sensor_icon = ""
                        sensor_label = ""
                        sensor_value = ""

                        match disp['tipo']:
                            case "termometro":
                                sensor_icon = "THERMOSTAT"
                                sensor_label = "Temperatura do\nambiente"
                                sensor_value = Text(value=str(json.loads(str(json.loads(disp['info'])))['temp']) + " °C", size=20)
                            case "gas":
                                sensor_icon = "GAS_METER"
                                sensor_label = datetime.strptime(disp['data_alteracao'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y\n%H:%M")
                                sensor_value = Text(value="Gás", size=20)
                            case "presenca":
                                sensor_icon = "EMOJI_PEOPLE"
                                #Formate a data_alteracao(2023-10-25T03.898296) para dd/mm/aaaa\nhh:mm
                                sensor_label = datetime.strptime(disp['data_alteracao'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d/%m/%Y\n%H:%M")
                                sensor_value = Text(value="Presença", size=15)

                        listaDisp.append(
                            ElevatedButton(
                                content=Container(
                                    Column(
                                        [
                                            Column(
                                                [
                                                    Row(
                                                        [
                                                            Icon(sensor_icon, size=30),
                                                            sensor_value,
                                                        ],
                                                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                    ),
                                                    Text(value=sensor_label, text_align=TextAlign.CENTER),
                                                ],
                                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                                expand=True,
                                            ),
                                        ],
                                        expand=True,
                                        #spacing=30
                                    ),
                                    #bgcolor=ft.colors.LIGHT_BLUE,
                                    margin=Margin(0,25,0,25),
                                ),
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                                #expand=True,
                                height=150,
                                width=150
                            ),
                        )

                    tela = Column(
                        [
                            Row(
                                listaDisp,
                                wrap=True,
                                alignment=MainAxisAlignment.SPACE_AROUND,
                            )
                        ],
                        horizontal_alignment=CrossAxisAlignment.STRETCH,
                        #visible=False
                        expand=True
                    )

                    #tela.controls = listaDisp
                    main.controls = [tela]
                    page.update()

            case "/dispositivos":
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=None, title=ft.Text("Dispositivos"), bgcolor=ft.colors.INDIGO)

                    listaDisp = []

                    dispositivos = sv_servidor.dispositivos_usr()

                    def go_to_add_dispositivo(e):
                        page.route = "/dispositivos/adicionar"
                        page.update()

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
                    main.controls = [tela]
                    page.floating_action_button = ft.FloatingActionButton(
                        icon=ft.icons.ADD,
                        on_click=go_to_add_dispositivo,
                        #bgcolor=ft.colors.LIME_300
                    )
                    page.update()

            case "/dispositivos/adicionar":
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=None, title=ft.Text("Adicionar dispositivo"), bgcolor=ft.colors.INDIGO)
                    page.floating_action_button = None

                    listaDisp = []

                    dispositivos = sv_servidor.dispositivos_usr()

                    residencias = sv_servidor.residencias_usr(page.session.get("token"))

                    resid_options = []

                    for resid in residencias:
                        resid_options.append(ft.dropdown.Option(resid['id'], resid['nome']))

                    try:
                        areas_resid = sv_servidor.areas_resid(page.session.get("token"), residencias[0]['id'])
                    except:
                        areas_resid = []

                    area_options = []

                    for area in areas_resid:
                        area_options.append(ft.dropdown.Option(area['id'], area['nome']))

                    def change_resid(e):
                        #print(e.control.value)
                        areas_resid = sv_servidor.areas_resid(page.session.get("token"), e.control.value)
                        area_options = []
                        for area in areas_resid:
                            area_options.append(ft.dropdown.Option(area['id'], area['nome']))
                        tela.controls[0].controls[4].options = area_options
                        tela.controls[0].controls[4].value = areas_resid[0]['id'] if len(areas_resid) > 0 else None
                        page.update()

                    def add_dispositivo(e):
                        print("Adicionar dispositivo")
                        page.navigation_bar.visible = False
                        page.appbar.visible = False
                        page.floating_action_button = None
                        main.controls = [
                            Column(
                                [
                                    Row(
                                        [
                                            Text("Dispositivo adicionado com sucesso!", size=45, text_align=TextAlign.CENTER, expand=True),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    )
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                expand=True
                            )
                        ]
                        page.update()
                        sleep(3000)
                        page.route = "/dispositivos"


                    tela = Column(
                        [
                            Column(
                                [
                                    ft.Dropdown(label="Tipo de dispositivo", options=[ft.dropdown.Option("termometro", "Termômetro"), ft.dropdown.Option("gas", "Sensor de gás"), ft.dropdown.Option("presenca", "Sensor de presença")], value="termometro"),
                                    ft.TextField(label="Nome do dispositivo"),
                                    ft.TextField(label="Código do dispositivo"),
                                    ft.Dropdown(label="Residência", options=resid_options, value=residencias[0]['id'] if len(residencias) > 0 else None, on_change=change_resid),
                                    ft.Dropdown(label="Área", options=area_options, value=areas_resid[0]['id'] if len(areas_resid) > 0 else None),
                                ]
                            ),
                            ElevatedButton(
                                content=Container(
                                    Row(
                                        [
                                            Text("Adicionar", size=30),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    margin=Margin(10,10,10,10),
                                ),
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                                on_click=add_dispositivo,
                            )
                        ],
                        #visible=False
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        expand=True
                    )

                    
                    main.controls = [tela]
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
                    main.controls = [tela]
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
                    main.controls = [tela]
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