from flet import(
    Column,
    Text,
    PopupMenuButton,
    PopupMenuItem,
    Row,
    Divider,
    Icon,
    icons,
    Container,
    ListView,
    margin,
    IconButton,
)

import navigation
import services

categorias = []
subcategorias = []

tela = Column(
    [
        ListView(
            spacing=5,
            #padding=20,
            expand=True,
            auto_scroll=False,
            #vertical=True,
            controls=categorias,
        ),
    ],
    expand=True,
    visible=False
)


def on_click_cat(e):
    index = int(e.control.key)
    print(index)

    if categorias[index].content.controls[1].visible == True:
        switch = False
    else:
        switch = True

    categorias[index].content.controls[1].visible = switch
    categorias[index].content.controls[1].content.visible = switch

    for item in categorias[index].content.controls[1].content.controls:

        item.visible = switch

    navigation.refresh()


#ind = 0


def onclick_item(e):
    navigation.ChangeScreen("21", e)

def load_cats():

    global categorias
    global subcategorias
    #global tela

    categorias = []
    ind = 0

    for cat in services.categorias.get_roots():

        subcategorias = []

        for subcat in services.categorias.get_subroots(cat.id):
            subcategorias.append(Divider(visible=False))
            subcategorias.append(
                Row(
                    [
                        Icon(
                            name=subcat.icone,
                        ),
                        Container(
                            Text(subcat.nome),
                            expand=True,
                        ),
                        IconButton(
                            icon=icons.EDIT_ROUNDED,
                            on_click=onclick_item,
                            key=subcat.id
                        ),
                    ],
                    visible=False
                )
            )


        categorias.append(
            Container(
                Column(
                    [
                        Container(
                            Row(
                                [
                                    Icon(
                                        name=cat.icone,
                                    ),
                                    Container(
                                        Text(cat.nome),
                                        expand=True,
                                        on_click=on_click_cat,
                                        key=ind
                                    ),
                                    IconButton(
                                        icon=icons.EDIT_ROUNDED,
                                        on_click=onclick_item,
                                        key=cat.id
                                    ),
                                ],
                            ),
                        ),
                        Container(
                            Column(subcategorias, visible=False),
                            visible=False,
                            margin = margin.only(left=20)
                        )
                    ]
                ),
            )
        )

        if len(categorias) > 0:
            categorias.append(Divider())

        ind += 2

    #tela.controls[0].controls = categorias
    return categorias

tela.controls[0].controls = load_cats()

def on_visible():
    global tela

    tela.controls[0].controls = load_cats()

    navigation.refresh()

navigation.paginas.append([tela,2,0,on_visible])