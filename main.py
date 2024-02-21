import flet as ft
import os

DEFAULT_FLET_PATH = ''
DEFAULT_FLET_PORT = 8522

#import pages

import navigation

import os

def main(page: ft.Page):

    paginas = navigation.paginas

    page.title = "Produtos"
    page.theme_mode = "DARK"

    #pages.configuracoes.main.page = page
    #pages.configuracoes.main.page.overlay.extend([pages.configuracoes.main.pick_files_dialog, pages.configuracoes.main.save_file_dialog, pages.configuracoes.main.get_directory_dialog])

    navigation.page = page

    page.appbar = ft.AppBar(
        leading = None,
        title=ft.Text("Produtos"),
        bgcolor=ft.colors.INDIGO,
    )

    def navigationBar(e):
        match e.control.selected_index:
            case 0:
                navigation.NavigationChange2("dispositivos")
            case 1:
                navigation.NavigationChange2("central")
            case 2:
                navigation.NavigationChange2("configuracoes")

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.PIE_CHART_OUTLINE_OUTLINED, selected_icon=ft.icons.PIE_CHART_OUTLINE, label="Dispositivos"),
            ft.NavigationDestination(icon=ft.icons.RECEIPT_LONG_OUTLINED, selected_icon=ft.icons.RECEIPT_LONG, label="Central"),
            #NavigationDestination(icon=ft.icons.SHOPPING_CART_OUTLINED, selected_icon=ft.icons.SHOPPING_CART, label="Produtos"),
            #NavigationDestination(icon=ft.icons.CATEGORY_OUTLINED, selected_icon=ft.icons.CATEGORY, label="Categorias"),
            ft.NavigationDestination(icon=ft.icons.ENGINEERING_OUTLINED, selected_icon=ft.icons.ENGINEERING, label="Configurações"),
        ],
        on_change = navigationBar,
    )

    page.navigation_bar.visible = True
    page.appbar.visible = True

    page.on_route_change = navigation.route_change

    #print(paginas)

    for pag in paginas:
        try:
            page.add(pag['objeto'])
        except:
            pass

    navigation.alterar_pagina()

if __name__ == "__main__":
    #flet_path = os.getenv("FLET_PATH", DEFAULT_FLET_PATH)
    flet_path =''
    flet_port = int(os.getenv("FLET_PORT", DEFAULT_FLET_PORT))
    ft.app(name=flet_path, target=main, view=None, port=flet_port)