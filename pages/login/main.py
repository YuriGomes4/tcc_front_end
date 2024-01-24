from flet import(
    Column,
    Row,
    Text,
    TextField,
    FilledButton,
    TextAlign,
    MainAxisAlignment,
    icons,
    Container,
    PieChartEvent,
    margin,
    IconButton,
    PieChart,
    PieChartSection
)

import navigation
import services.config as sv_config
import services.login as sv_login

def onclick_item(e):
    email = tela.controls[0].controls[1].controls[1].value
    senha = tela.controls[0].controls[1].controls[2].value

    sv_login.login(email, senha)
    #navigation.ChangeScreen("01", e)
    #pass

tela = Column(
    [
        Row(
            [
                Row(expand=True),
                Column(
                    [
                        Text(value="Login", size=50, width=250 ,text_align=TextAlign.CENTER),
                        TextField(hint_text="Email", width=250, value="teste@teste.com"),
                        TextField(hint_text="Password", width=250, password=True, can_reveal_password=True, value="teste123"),
                        FilledButton(content=Row([Text(value="ENTRAR", size=40,text_align=TextAlign.CENTER, expand=True),]), width=250, on_click=onclick_item)
                    ],
                ),
                Row(expand=True),
            ]
        ),
    ],
    alignment=MainAxisAlignment.CENTER,
    horizontal_alignment=MainAxisAlignment.CENTER,
    expand=True,
    visible=True
)

def on_visible():
    #global tela
    pass
    #tela.controls[0] = load_chart()
    #navigation.refresh()

navigation.paginas.append(
    {
        'objeto': tela,
        'numero': '@@',
        'vis_event': on_visible,
        'titulo': f"{sv_config.get('versao')} - Login",
    }
)