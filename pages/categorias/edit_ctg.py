from flet import(
    Column,
    Text,
    Container,
    Row,
    TextField,
    FilledTonalButton,
    IconButton,
    icons,
    alignment,
    KeyboardType,
)

import navigation
import services

save_temp = False

addit = "0"
cat_icone = IconButton(icon="add")
descricao = TextField(value='')

def onclick_item(e):
    global save_temp

    save_temp = True
    navigation.ChangeScreen("22", e)

def salvar_categoria(e):


    new_values = [descricao.value, cat_icone.icon]
    print("opa: ", descricao)

    services.categorias.modify_category_row(int(addit), new_values)

    navigation.BackScreen("")
    navigation.refresh()

tela = Column(
    [
        Container(
            Column(
                [
                    Row(
                        [
                            cat_icone
                        ]
                    ),
                    Row(
                        [
                            Text(f'Nome: '), descricao
                        ]
                    ),
                    Row(
                        [
                            FilledTonalButton("Salvar", on_click=salvar_categoria),
                            FilledTonalButton("Cancelar", on_click=navigation.BackScreen),
                        ]
                    ),
                ],
                expand=True
            )
        )
    ],
    visible=False
)

def on_visible():

    global addit
    global descricao
    global cat_icone
    global save_temp

    if str(navigation.addit)[0] == "@":
        cat_icone.icon = str(navigation.addit)[1:]

    if save_temp == False:
        addit = navigation.addit
        cat_icone.icon = services.categorias.get_cat(addit).icone
        cat_icone.on_click = onclick_item
        cat_icone.key = addit
        descricao.value = services.categorias.get_cat(addit).nome
    else:
        save_temp = False

    print(f"Opa: ", navigation.addit)

navigation.paginas.append([tela,2,1,on_visible])