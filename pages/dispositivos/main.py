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
    Margin,
    margin
)

import navigation
import services.config as sv_config
import services.servidor as sv_servidor

page = Page

tela = Column(
    [
        ListView()
    ],
    visible=False
)

def on_visible():

    listaDisp = []

    dispositivos = sv_servidor.dispositivos_usr()

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

navigation.paginas.append(
    {
        'objeto': tela,
        'numero': '00',
        'vis_event': on_visible,
        'titulo': f"{sv_config.get('versao')} - Dispositivos",
    }
)