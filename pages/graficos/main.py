from flet import(
    Column,
    TextStyle,
    FontWeight,
    colors,
    BoxShadow,
    border,
    Icon,
    icons,
    Container,
    PieChartEvent,
    margin,
    IconButton,
    PieChart,
    PieChartSection
)

import navigation
import services
import services.config as sv_config

chart = PieChart()

normal_radius = 80
hover_radius = 90
normal_title_style = TextStyle(
    size=12, color=colors.WHITE, weight=FontWeight.BOLD
)
hover_title_style = TextStyle(
    size=16,
    color=colors.WHITE,
    weight=FontWeight.BOLD,
    shadow=BoxShadow(blur_radius=2, color=colors.BLACK54),
)
normal_badge_size = 40
hover_badge_size = 50

def badge(icon, size):
    return Container(
        Icon(icon,color=colors.BLACK),
        width=size,
        height=size,
        border=border.all(1, colors.BROWN),
        border_radius=size / 2,
        bgcolor=colors.WHITE,
    )

def on_chart_event(e: PieChartEvent):
    for idx, section in enumerate(chart.sections):
        if idx == e.section_index:
            section.radius = hover_radius
            section.title_style = hover_title_style
        else:
            section.radius = normal_radius
            section.title_style = normal_title_style
    chart.update()

def load_chart():

    global transactions
    global cats
    global valores
    global total
    global secoes

    global chart
    #global tela

    transactions = []

    transactions = services.extrato.get_all()

    cats = []
    valores = []
    total = 0.0

    secoes = []

    for transaction in transactions:
        if transaction.tipo == "DEBIT":
            print(transaction.valor)
            total = total + float(str(transaction.valor).replace("-",""))

    print("Total:", total)

    for transaction in transactions:
        if not(transaction.categoria_id in cats) and transaction.tipo == "DEBIT":
            cats.append(transaction.categoria_id)
            valores.append(float(str(transaction.valor).replace("-","")))
        else:
            if transaction.tipo == "DEBIT":
                index = cats.index(transaction.categoria_id)
                valores[index] = valores[index] + float(str(transaction.valor).replace("-",""))

    print(cats)

    for ind in range(len(cats)):
        secoes.append(
            PieChartSection(
                valores[ind],
                title=f"{int((valores[ind] / total)*100)}%",
                title_style=normal_title_style,
                color=colors.BLUE,
                radius=normal_radius,
                badge=badge(services.categorias.get_cat(cats[ind]).icone, normal_badge_size),
                badge_position=0.98,
            )
        )


    chart.sections=secoes
    chart.sections_space=0
    chart.center_space_radius=40
    chart.on_chart_event=on_chart_event
    chart.expand=False

    return chart

tela = Column(
    [load_chart()],
    expand=True,
    visible=True
)

def on_visible():
    global tela
    tela.controls[0] = load_chart()
    navigation.refresh()

navigation.paginas.append(
    {
        'objeto': tela,
        'numero': '00',
        'vis_event': on_visible,
        'titulo': f"{sv_config.get('versao')} - Gráficos",
    }
)