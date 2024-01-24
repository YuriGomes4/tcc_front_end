from flet import(
    Container,
    Row,
    Icon,
    icons,
    Column,
    Text,
    MainAxisAlignment,
    TextAlign,
    ListView,
    colors,
)

from services import extrato as sv_extrato
from services import categorias as sv_categorias
import navigation

extratos = []

sv_extrato.parse_ofx_file_and_add_to_db("services/NU_3219096_01MAI2023_13MAI2023.ofx")

transactions = sv_extrato.get_all()
print(transactions[0])

def onclick_item(e):
    navigation.ChangeScreen("11", e)

for transaction in transactions:
    extratos.append(
        Container(
            Row(
                [
                    Icon(
                        name=sv_categorias.get_cat(transaction.categoria_id).icone,
                    ),
                    Column(
                        [
                            Text(transaction.descricao, text_align=TextAlign.LEFT, max_lines=1),
                            Text(sv_categorias.get_cat(transaction.categoria_id).nome, text_align=TextAlign.LEFT, max_lines=1),
                        ],
                        expand=True,
                        spacing=0,
                        alignment=MainAxisAlignment.CENTER,
                    ),
                    Text(f'R$: {transaction.valor}')
                ],
                expand=True
            ),
            on_click=onclick_item,
            key=f'{transaction.id}'
        )
    )

lista = ListView(
            spacing=5,
            #padding=20,
            expand=True,
            auto_scroll=False,
            #vertical=True,
            controls=extratos,
        )

tela = Column(
    [lista],
    #alignment=MainAxisAlignment.SPACE_AROUND,
    expand=True,
    visible=False
)

def on_visible():
    global transactions
    global extratos
    global lista

    extratos = []

    transactions = sv_extrato.get_all()

    for transaction in transactions:
        extratos.append(
            Container(
                Row(
                    [
                        Icon(
                            name=sv_categorias.get_cat(transaction.categoria_id).icone,
                            color=colors.AMBER
                        ),
                        Column(
                            [
                                Text(transaction.descricao, text_align=TextAlign.LEFT, max_lines=1),
                                Text(sv_categorias.get_cat(transaction.categoria_id).nome, text_align=TextAlign.LEFT, max_lines=1),
                            ],
                            expand=True,
                            spacing=0,
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        Text(f'R$: {"-" if transaction.tipo == "DEBIT" else ""}{str(transaction.valor).replace("-", "")}')
                    ],
                    expand=True
                ),
                on_click=onclick_item,
                key=f'{transaction.id}'
            )
        )
    
    lista.controls = extratos

    navigation.refresh()

navigation.paginas.append([tela,1,0,on_visible])