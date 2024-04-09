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
)

import navigation
import services.config as sv_config
import services.servidor as sv_servidor

#page = Page

def on_visible(page):

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

    #print(tela.controls[0].content.controls[0].content.width)

    page.add(tela)

navigation.paginas.append(
    {
        #'objeto': tela,
        'rota': 'central',
        'vis_event': on_visible,
        'titulo': f"{sv_config.get('versao')} - Central",
    }
)