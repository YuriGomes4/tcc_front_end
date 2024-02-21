from flet import(
    Column,
    Page,
    IconButton,
    icons,
    SnackBar,
    Text,
    RouteChangeEvent
)

#import pages

paginas = []
page = Page

addit = ""

tela = "@@"

def login(tela):
    pass

def alterar_pagina():
    global tela

    for pag in paginas:
        try:
            if str(pag['numero'][0]) == str(tela[0]) and str(pag['numero'][1]) == str(tela[1]):
                pag['objeto'].visible = True 
                page.title = pag['titulo']
                page.appbar.title.value = pag['titulo']
                print(f"Nova pagina é: {pag['titulo']}")
                try:
                    pag['vis_event']()
                except:
                    pass
            else:
                pag['objeto'].visible = False
        except:
            pass

    page.update()

def NavigationChange(e, screen=None):
    global tela
    
    if screen:
        tela = screen
        page.navigation_bar.visible = True
        page.appbar.visible = True
        index = screen
    else:
        index = e.control.selected_index

    tela = f"{index}{tela[1]}"

    alterar_pagina()

def BackScreen(e):
    global tela
    newScreen = int(tela[1])-1

    if newScreen == 0:
        page.appbar.leading = None
        page.navigation_bar.visible = True

    tela = f"{tela[0]}{newScreen}"

    alterar_pagina()

def ChangeScreen(screen, e):
    global addit
    global tela
    tela = screen
    page.appbar.leading = IconButton(
        icon = icons.ARROW_BACK,
        on_click = BackScreen,
    )
    page.navigation_bar.visible = False

    addit = e.control.key

    alterar_pagina()

def route_change(e: RouteChangeEvent):
    print(e.route)
    #page.views.clear()
    page.add(Text(f"New route: {e.route}"))

def NavigationChange2(route):
    page.route = route
    page.update()

def notify(texto):
    page.snack_bar = SnackBar(Text(texto))
    page.snack_bar.open = True
    page.update()

def refresh():
    page.update()