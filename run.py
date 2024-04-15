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

    page.session.set("token", "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9wdWJsaWNvIjoiYzkxNGQzOWYtNDc1Yy00NWMzLTgzYTgtYTM1ODFmMzNkOTQwIn0.AUkj4ipNLF46vqMRul51Jgd6AdX2HbBpxDowSzOIIOo")
    #page.session.set("token", "aaa")

    #page.bgcolor = ft.colors.WHITE24
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=ft.colors.GREEN_ACCENT)

    page.appbar = ft.AppBar(
        leading = None,
        title=ft.Text("Produtos"),
        #bgcolor=ft.colors.GREEN_400,
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
            ft.NavigationDestination(icon=ft.icons.BROADCAST_ON_HOME_ROUNDED, selected_icon=ft.icons.BROADCAST_ON_HOME_ROUNDED, label="Dispositivos"),
            ft.NavigationDestination(icon=ft.icons.GRID_VIEW_OUTLINED, selected_icon=ft.icons.GRID_VIEW_SHARP, label="Central"),
            #NavigationDestination(icon=ft.icons.SHOPPING_CART_OUTLINED, selected_icon=ft.icons.SHOPPING_CART, label="Produtos"),
            #NavigationDestination(icon=ft.icons.CATEGORY_OUTLINED, selected_icon=ft.icons.CATEGORY, label="Categorias"),
            ft.NavigationDestination(icon=ft.icons.SETTINGS_OUTLINED, selected_icon=ft.icons.SETTINGS, label="Configurações"),
        ],
        on_change = on_change_navbar,
        selected_index=1,
        #bgcolor=ft.colors.GREEN_ACCENT,
    )

    page.navigation_bar.visible = False
    page.appbar.visible = False
    page.appbar = ft.AppBar(leading=None, title=ft.Text("Aplicativo"), bgcolor=ft.colors.GREEN_400)
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
                #page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Residencias"), bgcolor=ft.colors.GREEN_400)

                def login(e):
                    email = tela.controls[0].controls[0].controls[1].value
                    senha = tela.controls[0].controls[0].controls[2].value

                    token = sv_servidor.login(email, senha)

                    if token:
                        page.session.set("token", token)
                        page.route = "/central"
                        page.update()
                    else:
                        page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Email ou senha inválidos!"))
                        page.update()

                def go_to_criar_conta(e):
                    page.route = "/criar_conta"
                    page.update()

                tela = Column(
                    [
                        Row(
                            [
                                Column(
                                    [
                                        ft.Text("APP", size=50, color=ft.colors.PRIMARY),
                                        ft.TextField(label="Email"),
                                        ft.TextField(label="Senha", password=True, can_reveal_password=True),
                                        ft.ElevatedButton(
                                            content=Container(
                                                Row(
                                                    [
                                                        Text("Entrar", size=30),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                ),
                                                margin=Margin(10,10,10,10),
                                                expand=True
                                            ),
                                            style=ButtonStyle(
                                                shape=RoundedRectangleBorder(radius=10),
                                                #color=ft.colors.WHITE,
                                                #bgcolor=ft.colors.GREEN_400
                                            ),
                                            on_click=login
                                        ),
                                        ft.TextButton(
                                            "Não tenho uma conta",
                                            on_click=go_to_criar_conta,
                                            #style=ButtonStyle(overlay_color=ft.colors.with_opacity(0, ft.colors.GREEN_400), color=ft.colors.GREEN_400)
                                        )
                                    ],
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            expand=True
                        )
                    ],
                    #visible=False
                    alignment=MainAxisAlignment.CENTER,
                    expand=True
                )

                #tela.controls = nova_tela
                main.controls = [tela]
                page.update()

            case "/criar_conta":
                page.navigation_bar.visible = False
                page.appbar.visible = False
                #page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Residencias"), bgcolor=ft.colors.GREEN_400)

                def criar_conta(e):
                    nome = tela.controls[0].controls[0].controls[1].value
                    email = tela.controls[0].controls[0].controls[2].value
                    senha = tela.controls[0].controls[0].controls[3].value

                    if sv_servidor.criar_conta(nome, email, senha):
                        page.route = "/login"
                        page.update()
                    else:
                        page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao criar conta!"))
                        page.update()

                tela = Column(
                    [
                        Row(
                            [
                                Column(
                                    [
                                        ft.Text("Criar uma conta", size=40, color=ft.colors.PRIMARY),
                                        ft.TextField(label="Nome"),
                                        ft.TextField(label="Email"),
                                        ft.TextField(label="Senha", password=True, can_reveal_password=True),
                                        ft.ElevatedButton(
                                            content=Container(
                                                Row(
                                                    [
                                                        Text("Criar conta", size=30),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                ),
                                                margin=Margin(10,10,10,10),
                                                expand=True
                                            ),
                                            style=ButtonStyle(
                                                shape=RoundedRectangleBorder(radius=10),
                                                #color=ft.colors.WHITE,
                                                #bgcolor=ft.colors.GREEN_400
                                            ),
                                            on_click=criar_conta
                                        )
                                    ],
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    alignment=MainAxisAlignment.CENTER,
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            expand=True
                        )
                    ],
                    #visible=False
                    alignment=MainAxisAlignment.CENTER,
                    expand=True
                )

                #tela.controls = nova_tela
                main.controls = [tela]
                page.update()

            case "/central":
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    #page.appbar = ft.AppBar(leading=None, title=ft.Text("Central"), bgcolor=ft.colors.GREEN_400)
                    page.appbar.leading = None
                    page.appbar.title = ft.Text("Central")
                    page.floating_action_button = None
                    listaDisp = []

                    dispositivos = sv_servidor.dispositivos_usr(page.session.get("token"))

                    if len(dispositivos) > 0:

                        for disp in dispositivos:

                            sensor_icon = ""
                            sensor_label = ""
                            sensor_value = ""

                            match disp['tipo']:
                                case "termometro":
                                    sensor_icon = "THERMOSTAT"
                                    sensor_label = "Temperatura do\nambiente"
                                    sensor_value = Text(value=str(disp['info']['temp']) + " °C", size=20)
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

                    else:
                        tela = Column(
                            [
                                Row(
                                    [
                                        Text('Nenhum dispositivo cadastrado!\nVá para "Dispositivos" e cadastre um.', size=30, text_align=TextAlign.CENTER, expand=True),
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                )
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            expand=True
                        )

                    #tela.controls = listaDisp
                    main.controls = [tela]
                    page.update()

            case "/dispositivos":
                if verify_token():
                    page.navigation_bar.visible = True
                    page.appbar.visible = True
                    #page.appbar = ft.AppBar(leading=None, title=ft.Text("Dispositivos"))
                    page.appbar.leading = None
                    page.appbar.title = ft.Text("Dispositivos")

                    listaDisp = []

                    dispositivos = sv_servidor.dispositivos_usr(page.session.get("token"))

                    def go_to_add_dispositivo(e):
                        page.route = "/dispositivos/adicionar"
                        page.update()

                    def go_to_ver_dispositivo(e):
                        page.route = f"/dispositivos/ver{e.control.key}"
                        page.update()

                    tela = Column(
                        [
                            ListView()
                        ],
                        #visible=False
                    )

                    if len(dispositivos) > 0:

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
                                        key=disp['id'],
                                        on_click=go_to_ver_dispositivo
                                    )
                                )
                            )

                        tela.controls = listaDisp
                        page.floating_action_button = ft.FloatingActionButton(
                            icon=ft.icons.ADD,
                            on_click=go_to_add_dispositivo,
                            #bgcolor=ft.colors.LIME_300
                        )
                    else:
                        areas = sv_servidor.ver_areas(page.session.get("token"))

                        if len(areas) > 0:

                            tela = Column(
                                [
                                    Row(
                                        [
                                            Text('Nenhum dispositivo cadastrado!', size=30, text_align=TextAlign.CENTER, expand=True),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    )
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                expand=True
                            )

                            page.floating_action_button = ft.FloatingActionButton(
                                icon=ft.icons.ADD,
                                on_click=go_to_add_dispositivo,
                                #bgcolor=ft.colors.LIME_300
                            )

                        else:
                            tela = Column(
                                [
                                    Row(
                                        [
                                            Text('Você não pode cadastrar dispositivos\nsem ter uma residência e áreas!\nVá em Configurações > Residências > Escolha uma > Editar áreas', size=30, text_align=TextAlign.CENTER, expand=True),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    )
                                ],
                                alignment=MainAxisAlignment.CENTER,
                                horizontal_alignment=CrossAxisAlignment.CENTER,
                                expand=True
                            )

                            page.floating_action_button = None

                    main.controls = [tela]
                    page.update()

            case "/dispositivos/adicionar":
                if verify_token():
                    page.navigation_bar.visible = False
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Adicionar dispositivo"), bgcolor=ft.colors.GREEN_400)
                    page.floating_action_button = None

                    listaDisp = []

                    dispositivos = sv_servidor.dispositivos_usr(page.session.get("token"))

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

                        tipo = tela.controls[0].controls[0].value
                        nome = tela.controls[0].controls[1].value
                        codigo = tela.controls[0].controls[2].value
                        residencia = tela.controls[0].controls[3].value
                        area = tela.controls[0].controls[4].value

                        if sv_servidor.add_dispositivo(page.session.get("token"), tipo, nome, codigo, residencia, area):

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
                            sleep(3)
                            page.route = "/dispositivos"
                            page.update()
                        else:
                            page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao adicionar dispositivo!"))
                            page.update()


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
                    #page.appbar = ft.AppBar(leading=None, title=ft.Text("Configurações"), bgcolor=ft.colors.GREEN_400)
                    page.appbar.leading = None
                    page.appbar.title = ft.Text("Configurações")
                    page.floating_action_button = None

                    def go_to_residencias(e):
                        page.route = "/configuracoes/residencias"
                        page.update()

                    def go_to_conta(e):
                        page.route = "/configuracoes/conta"
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
                                                            on_click=go_to_conta,
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
                    page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Residencias"), bgcolor=ft.colors.GREEN_400)

                    def go_to_add_residencia(e):
                        page.route = "/configuracoes/residencias/adicionar"
                        page.update()

                    def go_to_ver_residencia(e):
                        page.route = f"/configuracoes/residencias/ver{e.control.key}"
                        page.update()

                    page.floating_action_button = ft.FloatingActionButton(
                        icon=ft.icons.ADD,
                        on_click=go_to_add_residencia,
                    )

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
                                    key=resid['id'],
                                    on_click=go_to_ver_residencia
                                )
                            )
                        )

                    tela.content.controls = listaResids

                    #tela.controls = nova_tela
                    main.controls = [tela]
                    page.update()

            case "/configuracoes/residencias/adicionar":
                if verify_token():
                    page.navigation_bar.visible = False
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Adicionar residência"), bgcolor=ft.colors.GREEN_400)
                    page.floating_action_button = None

                    def add_residencia(e):
                        print("Adicionar residencia")

                        nome = tela.controls[0].controls[0].value

                        if sv_servidor.add_residencia(page.session.get("token"), nome):

                            page.navigation_bar.visible = False
                            page.appbar.visible = False
                            page.floating_action_button = None
                            main.controls = [
                                Column(
                                    [
                                        Row(
                                            [
                                                Text("Residência adicionada com sucesso!", size=45, text_align=TextAlign.CENTER, expand=True),
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
                            sleep(3)
                            page.route = "/configuracoes/residencias"
                            page.update()
                        else:
                            page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao adicionar residência!"))
                            page.update()

                    tela = Column(
                        [
                            Column(
                                [
                                    ft.TextField(label="Nome da residência"),
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
                                on_click=add_residencia,
                            )
                        ],
                        #visible=False
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        expand=True
                    )

                    main.controls = [tela]
                    page.update()

            case "/configuracoes/conta":
                if verify_token():
                    page.navigation_bar.visible = False
                    page.appbar.visible = True
                    page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Conta"), bgcolor=ft.colors.GREEN_400)
                    page.floating_action_button = None

                    usuario = sv_servidor.ver_usuario(page.session.get("token"))

                    def salvar_conta(e):
                        nome = tela.controls[0].controls[1].value
                        email = tela.controls[0].controls[2].value
                        senha = tela.controls[0].controls[3].value

                        if sv_servidor.editar_usuario(page.session.get("token"), nome, email, senha):
                                
                                page.navigation_bar.visible = False
                                page.appbar.visible = False
                                page.floating_action_button = None
                                main.controls = [
                                    Column(
                                        [
                                            Row(
                                                [
                                                    Text("Conta salva com sucesso!", size=45, text_align=TextAlign.CENTER, expand=True),
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
                                sleep(3)
                                page.route = "/configuracoes"
                                page.update()
                        else:
                            page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao salvar conta!"))
                            page.update()

                    tela = Column(
                        [
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
                                    ft.TextField(label="Nome", value=usuario['nome']),
                                    ft.TextField(label="Email", value=usuario['email']),
                                    ft.TextField(label="Nova senha", password=True, can_reveal_password=True),
                                ]
                            ),
                            ElevatedButton(
                                content=Container(
                                    Row(
                                        [
                                            Text("Salvar", size=30),
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                    ),
                                    margin=Margin(10,10,10,10),
                                ),
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                                on_click=salvar_conta,
                            )
                        ],
                        #visible=False
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        expand=True
                    )

                    main.controls = [tela]
                    page.update()

            case _:
                if e.route.startswith("/dispositivos/ver"):
                    if verify_token():
                        id_disp = int(e.route.replace("/dispositivos/ver", ""))

                        dispositivo = sv_servidor.ver_dispositivo(page.session.get("token"), id_disp)

                        page.navigation_bar.visible = False
                        page.appbar.visible = True
                        page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Ver dispositivo"), bgcolor=ft.colors.GREEN_400)
                        page.floating_action_button = None

                        listaDisp = []

                        #dispositivos = sv_servidor.dispositivos_usr(token)

                        residencias = sv_servidor.residencias_usr(page.session.get("token"))

                        resid_options = []

                        for resid in residencias:
                            resid_options.append(ft.dropdown.Option(resid['id'], resid['nome']))

                        try:
                            areas_resid = sv_servidor.areas_resid(page.session.get("token"), dispositivo['id_residencia'])
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

                        def excluir_dispositivo(e):
                            sv_servidor.excluir_dispositivo(page.session.get("token"), id_disp)
                            page.route = "/dispositivos"
                            page.update()

                        def salvar_edicao(e):
                            nome = tela.controls[0].controls[1].value
                            codigo = tela.controls[0].controls[2].value
                            id_residencia = tela.controls[0].controls[3].value
                            id_area_residencia = tela.controls[0].controls[4].value

                            if sv_servidor.editar_dispositivo(page.session.get("token"), id_disp, nome, codigo, id_residencia, id_area_residencia):

                                #Desfaça as alterações feitas no layout por editar_dispositivo
                                tela.controls[1].controls[1].visible = True
                                tela.controls[1].controls[0].content.content.controls[0].value = "Editar"
                                #tela.controls[1].controls[0].style.bgcolor = ft.colors.SECONDARY
                                tela.controls[1].controls[0].on_click = editar_dispositivo

                                tela.controls[0].controls[1].disabled = True
                                tela.controls[0].controls[2].disabled = True
                                tela.controls[0].controls[3].disabled = True
                                tela.controls[0].controls[4].disabled = True

                                page.update()

                            else:
                                page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao editar dispositivo!"))
                                page.update()

                        def editar_dispositivo(e):
                            
                            #Tire a visibilidade do botão escluir
                            tela.controls[1].controls[1].visible = False

                            #Mude o texto do botão editar para salvar, a cor para verde e o on_click para salvar_edicao
                            tela.controls[1].controls[0].content.content.controls[0].value = "Salvar"
                            #tela.controls[1].controls[0].style.bgcolor = ft.colors.GREEN
                            tela.controls[1].controls[0].on_click = salvar_edicao

                            #Habilite os campos para edição
                            tela.controls[0].controls[1].disabled = False
                            tela.controls[0].controls[2].disabled = False
                            tela.controls[0].controls[3].disabled = False
                            tela.controls[0].controls[4].disabled = False

                            page.update()


                        tela = Column(
                            [
                                Column(
                                    [
                                        ft.Dropdown(label="Tipo de dispositivo", options=[ft.dropdown.Option("termometro", "Termômetro"), ft.dropdown.Option("gas", "Sensor de gás"), ft.dropdown.Option("presenca", "Sensor de presença")], value=dispositivo['tipo'], disabled=True),
                                        ft.TextField(label="Nome do dispositivo", disabled=True, value=dispositivo['nome']),
                                        ft.TextField(label="Código do dispositivo", disabled=True, value=dispositivo['codigo']),
                                        ft.Dropdown(label="Residência", options=resid_options, on_change=change_resid, disabled=True, value=dispositivo['id_residencia']),
                                        ft.Dropdown(label="Área", options=area_options, value=dispositivo['id_area_residencia'], disabled=True),
                                    ]
                                ),
                                Column(
                                    [
                                        ElevatedButton(
                                            content=Container(
                                                Row(
                                                    [
                                                        Text("Editar", size=30),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                ),
                                                margin=Margin(10,10,10,10),
                                            ),
                                            style=ButtonStyle(
                                                shape=RoundedRectangleBorder(radius=10),
                                                #bgcolor=ft.colors.BLUE
                                            ),
                                            on_click=editar_dispositivo
                                        ),
                                        ElevatedButton(
                                            content=Container(
                                                Row(
                                                    [
                                                        Text("Excluir", size=25),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                ),
                                                margin=Margin(7,7,7,7),
                                            ),
                                            style=ButtonStyle(
                                                shape=RoundedRectangleBorder(radius=10),
                                                bgcolor=ft.colors.RED,
                                                color=ft.colors.WHITE
                                            ),
                                            on_click=excluir_dispositivo
                                        )
                                    ]
                                )
                            ],
                            #visible=False
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            expand=True
                        )

                        main.controls = [tela]
                        page.update()

                elif e.route.startswith("/configuracoes/residencias/ver"):
                    if verify_token():
                        id_resid = int(e.route.replace("/configuracoes/residencias/ver", ""))

                        residencia = sv_servidor.ver_residencia(page.session.get("token"), id_resid)

                        page.navigation_bar.visible = False
                        page.appbar.visible = True
                        page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Ver residência"), bgcolor=ft.colors.GREEN_400)
                        page.floating_action_button = None

                        areas_resid = sv_servidor.areas_resid(page.session.get("token"), id_resid)

                        def excluir_residencia(e):
                            sv_servidor.excluir_residencia(page.session.get("token"), id_resid)
                            page.route = "/configuracoes/residencias"
                            page.update()

                        def salvar_edicao(e):
                            nome = tela.controls[0].controls[0].value

                            if sv_servidor.editar_residencia(page.session.get("token"), id_resid, nome):

                                #Desfaça as alterações feitas no layout por editar_residencia
                                tela.controls[1].controls[1].visible = True
                                tela.controls[1].controls[0].content.content.controls[0].value = "Editar"
                                #tela.controls[1].controls[0].style.bgcolor = ft.colors.SECONDARY
                                tela.controls[1].controls[0].on_click = editar_residencia

                                tela.controls[0].controls[0].disabled = True

                                page.update()

                            else:
                                page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao editar residência!"))
                                page.update()

                        def editar_residencia(e):
                            
                            #Tire a visibilidade do botão escluir
                            tela.controls[1].controls[1].visible = False

                            #Mude o texto do botão editar para salvar, a cor para verde e o on_click para salvar_edicao
                            tela.controls[1].controls[0].content.content.controls[0].value = "Salvar"
                            #tela.controls[1].controls[0].style.bgcolor = ft.colors.GREEN
                            tela.controls[1].controls[0].on_click = salvar_edicao

                            #Habilite os campos para edição
                            tela.controls[0].controls[0].disabled = False

                            page.update()

                        def go_to_editar_areas(e):
                            page.route = f"/configuracoes/residencias/areas{id_resid}"
                            page.update()

                        tela = Column(
                            [
                                Column(
                                    [
                                        ft.TextField(label="Nome da residência", disabled=True, value=residencia['nome']),
                                        ft.ElevatedButton(
                                            content=Container(
                                                Row(
                                                    [
                                                        Text("Editar areas", size=20),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                ),
                                                margin=Margin(6,6,6,6),
                                            ),
                                            style=ButtonStyle(
                                                shape=RoundedRectangleBorder(radius=10),
                                            ),
                                            on_click=go_to_editar_areas,
                                        )
                                    ]
                                ),
                                Column(
                                    [
                                        ElevatedButton(
                                            content=Container(
                                                Row(
                                                    [
                                                        Text("Editar", size=30),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                ),
                                                margin=Margin(10,10,10,10),
                                            ),
                                            style=ButtonStyle(
                                                shape=RoundedRectangleBorder(radius=10),
                                                #bgcolor=ft.colors.BLUE
                                            ),
                                            on_click=editar_residencia
                                        ),
                                        ElevatedButton(
                                            content=Container(
                                                Row(
                                                    [
                                                        Text("Excluir", size=25),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                ),
                                                margin=Margin(7,7,7,7),
                                            ),
                                            style=ButtonStyle(
                                                shape=RoundedRectangleBorder(radius=10),
                                                bgcolor=ft.colors.RED,
                                                color=ft.colors.WHITE
                                            ),
                                            on_click=excluir_residencia
                                        )
                                    ]
                                )
                            ],
                            #visible=False
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            expand=True
                        )

                        main.controls = [tela]
                        page.update()

                elif e.route.startswith("/configuracoes/residencias/areas"):
                    if not e.route.__contains__("editarea"):
                        if verify_token():  
                            id_resid = int(e.route.replace("/configuracoes/residencias/areas", ""))

                            residencia = sv_servidor.ver_residencia(page.session.get("token"), id_resid)

                            page.navigation_bar.visible = False
                            page.appbar.visible = True
                            page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Editar áreas da residência"), bgcolor=ft.colors.GREEN_400)

                            def go_to_add_area(e):
                                page.route = f"/configuracoes/residencias/addarea{id_resid}"
                                page.update()

                            page.floating_action_button = ft.FloatingActionButton(
                                icon=ft.icons.ADD,
                                on_click=go_to_add_area,
                            )

                            def go_to_editar_area(e):
                                id_area = e.control.key
                                page.route = f"/configuracoes/residencias/areas{id_resid}/editarea{id_area}"
                                page.update()

                            areas_resid = sv_servidor.areas_resid(page.session.get("token"), id_resid)

                            tela = Column(
                                [
                                    ListView()
                                ],
                                expand=True
                            )

                            nova_tela = []

                            for area in areas_resid:
                                nova_tela.append(
                                    ElevatedButton(
                                        content=Container(
                                            Row(
                                                [
                                                    Icon("home"),
                                                    Column(
                                                        [
                                                            Text(value=area['nome'], size=20),
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
                                        key=area['id'],
                                        on_click=go_to_editar_area
                                    )
                                )

                            tela.controls = nova_tela

                            main.controls = [tela]
                            page.update()

                    else:
                        if verify_token():
                            route_split = e.route.split("/")
                            id_area = int(route_split[4].replace("editarea", ""))
                            id_resid = int(route_split[3].replace("areas", ""))

                            #page.route = f"/configuracoes/residencias/areas{id_resid}/editarea{id_area}"

                            area = sv_servidor.ver_area(page.session.get("token"), id_area)

                            page.navigation_bar.visible = False
                            page.appbar.visible = True
                            page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Editar área"), bgcolor=ft.colors.GREEN_400)
                            page.floating_action_button = None

                            def excluir_area(e):
                                sv_servidor.excluir_area(page.session.get("token"), id_area)
                                page.route = f"/configuracoes/residencias/areas{id_resid}"
                                page.update()

                            def salvar_edicao(e):
                                nome = tela.controls[0].controls[0].value

                                if sv_servidor.editar_area(page.session.get("token"), id_area, nome):

                                    #Desfaça as alterações feitas no layout por editar_residencia
                                    tela.controls[1].controls[1].visible = True
                                    tela.controls[1].controls[0].content.content.controls[0].value = "Editar"
                                    #tela.controls[1].controls[0].style.bgcolor = ft.colors.SECONDARY
                                    tela.controls[1].controls[0].on_click = editar_area

                                    tela.controls[0].controls[0].disabled = True

                                    page.update()

                                else:
                                    page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao editar área!"))
                                    page.update()

                            def editar_area(e):
                                
                                #Tire a visibilidade do botão escluir
                                tela.controls[1].controls[1].visible = False

                                #Mude o texto do botão editar para salvar, a cor para verde e o on_click para salvar_edicao
                                tela.controls[1].controls[0].content.content.controls[0].value = "Salvar"
                                #tela.controls[1].controls[0].style.bgcolor = ft.colors.GREEN
                                tela.controls[1].controls[0].on_click = salvar_edicao

                                #Habilite os campos para edição
                                tela.controls[0].controls[0].disabled = False

                                page.update()

                            tela = Column(
                                [
                                    Column(
                                        [
                                            ft.TextField(label="Nome da área", disabled=True, value=area['nome']),
                                        ]
                                    ),
                                    Column(
                                        [
                                            ElevatedButton(
                                                content=Container(
                                                    Row(
                                                        [
                                                            Text("Editar", size=30),
                                                        ],
                                                        alignment=MainAxisAlignment.CENTER,
                                                    ),
                                                    margin=Margin(10,10,10,10),
                                                ),
                                                style=ButtonStyle(
                                                    shape=RoundedRectangleBorder(radius=10),
                                                    #bgcolor=ft.colors.BLUE
                                                ),
                                                on_click=editar_area
                                            ),
                                            ElevatedButton(
                                                content=Container(
                                                    Row(
                                                        [
                                                            Text("Excluir", size=25),
                                                        ],
                                                        alignment=MainAxisAlignment.CENTER,
                                                    ),
                                                    margin=Margin(7,7,7,7),
                                                ),
                                                style=ButtonStyle(
                                                    shape=RoundedRectangleBorder(radius=10),
                                                    bgcolor=ft.colors.RED,
                                                    color=ft.colors.WHITE
                                                ),
                                                on_click=excluir_area
                                            )
                                        ]
                                    )
                                ],
                                #visible=False
                                alignment=MainAxisAlignment.SPACE_BETWEEN,
                                expand=True
                            )

                            main.controls = [tela]
                            page.update()


                elif e.route.startswith("/configuracoes/residencias/addarea"):
                    if verify_token():
                        id_resid = int(e.route.replace("/configuracoes/residencias/addarea", ""))

                        #residencia = sv_servidor.ver_residencia(page.session.get("token"), id_resid)

                        page.navigation_bar.visible = False
                        page.appbar.visible = True
                        #page.appbar = ft.AppBar(leading=ft.IconButton(icon=icons.ARROW_BACK, on_click=back), title=ft.Text("Adicionar área"), bgcolor=ft.colors.GREEN_400)
                        page.appbar.leading = ft.IconButton(icon=icons.ARROW_BACK, on_click=back)
                        page.appbar.title = ft.Text("Adicionar área")
                        page.floating_action_button = None

                        def add_area(e):
                            print("Adicionar area")

                            nome = tela.controls[0].controls[0].value

                            if sv_servidor.add_area(page.session.get("token"), nome, id_resid):

                                page.navigation_bar.visible = False
                                page.appbar.visible = False
                                page.floating_action_button = None
                                main.controls = [
                                    Column(
                                        [
                                            Row(
                                                [
                                                    Text("Área adicionada com sucesso!", size=45, text_align=TextAlign.CENTER, expand=True),
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
                                sleep(3)
                                page.route = f"/configuracoes/residencias/areas{id_resid}"
                                page.update()
                            else:
                                page.dialog = ft.AlertDialog(open=True, title=Text("Erro"), content=Text("Erro ao adicionar área!"))
                                page.update()

                        tela = Column(
                            [
                                Column(
                                    [
                                        ft.TextField(label="Nome da área"),
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
                                    on_click=add_area,
                                )
                            ],
                            #visible=False
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            expand=True
                        )

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