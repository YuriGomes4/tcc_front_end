from flet import(
    Column,
    Text,
    Container,
    Row,
    TextField,
    FilledTonalButton,
    Dropdown,
    dropdown,
    KeyboardType,
)

import navigation
import services
from .main import transactions

save_temp = False

addit = ""

id = Text(f'')
descricao = TextField(value='')
valor = TextField(keyboard_type=KeyboardType.NUMBER)
tipo = Dropdown(options=[dropdown.Option("DEBIT"), dropdown.Option("CREDIT")])
data = Text(f'')
categoria = FilledTonalButton("")


for transaction in transactions:
    if transaction.id == addit:
        id.value = f'{transaction.id}'
        descricao.value = f'{transaction.descricao}'
        valor.value = f'{transaction.valor}'
        tipo.value = f'{transaction.tipo}'
        data.value = f'{transaction.data}'
        categoria.text = transaction.categoria.nome

def salvar_extrato(e):


    new_values = [descricao.value, valor.value, tipo.value, data.value, categoria.key]
    print("opa: ", descricao)

    services.extrato.modify_extrato_row(id.value, new_values)

    navigation.BackScreen("")

def onclick_item(e):
    navigation.ChangeScreen("12", e)

    

tela = Column(
    [
        Container(
            Column(
                [
                    Row(
                        [
                            Text(f'ID: '), id
                        ]
                    ),
                    Row(
                        [
                            Text(f'Descrição: '), descricao
                        ]
                    ),
                    Row(
                        [
                            Text(f'Valor: '), valor
                        ]
                    ),
                    Row(
                        [
                            Text(f'Data: '), data
                        ]
                    ),
                    Row(
                        [
                            Text(f'Tipo: '), tipo
                        ]
                    ),
                    Row(
                        [
                            Text(f'Categoria: '), categoria
                        ]
                    ),
                    Row(
                        [
                            FilledTonalButton("Salvar", on_click=salvar_extrato),
                            FilledTonalButton("Cancelar", on_click=navigation.BackScreen),
                        ]
                    ),
                    
                ]
            )
        )
    ],
    visible=False
)

def on_visible():
    global addit
    global id
    global descricao
    global valor
    global tipo
    global data

    global save_temp

    if str(navigation.addit)[0] == "@":
        categoria.text = services.categorias.get_cat(int(str(navigation.addit)[1:])).nome
        categoria.on_click = onclick_item
        categoria.key = int(str(navigation.addit)[1:])

    if save_temp == False:
        addit = navigation.addit
        
        all = services.extrato.get_all()

        for transaction in all:
            if transaction.id == addit:
                id.value = transaction.id
                descricao.value = transaction.descricao
                valor.value = str(transaction.valor).replace("-", "")
                tipo.value = transaction.tipo
                data.value = transaction.data
                categoria.text = transaction.categoria.nome
                categoria.on_click = onclick_item
                categoria.key = transaction.categoria_id
    else:
        save_temp = False


    print(f"Opa: {addit}")

navigation.paginas.append([tela,1,1,on_visible])
