from flet import(
    app,
    Page,
    AppBar,
    colors,
    NavigationBar,
    Text,
    icons,
    NavigationDestination,
    Column,
    Container,
    Row,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    IconButton,
)


def main(page: Page):

    page.title = "NavigationBar Example"

    # Pick files dialog
    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        selected_files.update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()

    # Save file dialog
    def save_file_result(e: FilePickerResultEvent):
        save_file_path.value = e.path if e.path else "Cancelled!"
        save_file_path.update()

    save_file_dialog = FilePicker(on_result=save_file_result)
    save_file_path = Text()

    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()

    # hide all dialogs in overlay
    page.overlay.extend([pick_files_dialog, save_file_dialog, get_directory_dialog])

    def NavigationChange(e):
        index = e.control.selected_index
        tela1.visible = True if index == 0 else False
        tela2.visible = True if index == 1 else False
        tela3.visible = True if index == 2 else False
        page.update()

    def ScreenChange(e):
        tela1.visible = True
        tela2.visible = False
        tela3.visible = False
        page.update()

    tela1 = Column(
        [
            Row(
                [
                    ElevatedButton(
                        "Pick files",
                        icon=icons.UPLOAD_FILE,
                        on_click=lambda _: pick_files_dialog.pick_files(
                            allow_multiple=True
                        ),
                    ),
                    selected_files,
                ]
            ),
            Row(
                [
                    ElevatedButton(
                        "Save file",
                        icon=icons.SAVE,
                        on_click=lambda _: save_file_dialog.save_file(),
                        disabled=page.web,
                    ),
                    save_file_path,
                ]
            ),
            Row(
                [
                    ElevatedButton(
                        "Open directory",
                        icon=icons.FOLDER_OPEN,
                        on_click=lambda _: get_directory_dialog.get_directory_path(),
                        disabled=page.web,
                    ),
                    directory_path,
                ]
            ),
        ]
    )

    tela2 = Column(
        [
            Text("Porra")
        ],
        visible=False
    )

    tela3 = Column(
        [
            Text("Caralho")
        ],
        visible=False
    )

    page.appbar = AppBar(
        leading = IconButton(
            icon = icons.ARROW_BACK,
            on_click = ScreenChange,
        ),
        title=Text("Flet app"),
        bgcolor=colors.INDIGO,
    )
    page.navigation_bar = NavigationBar(
        destinations=[
            NavigationDestination(icon=icons.EXPLORE, label="Explore"),
            NavigationDestination(icon=icons.COMMUTE, label="Commute"),
            NavigationDestination(
                icon=icons.BOOKMARK_BORDER,
                selected_icon=icons.BOOKMARK,
                label="Explore",
            ),
        ],
        on_change = NavigationChange,
    )

    page.add(tela1, tela2, tela3)


app(target=main)