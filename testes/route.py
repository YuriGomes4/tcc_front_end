import flet
from flet import (
    AppBar, 
    ElevatedButton, 
    Page, 
    Text, 
    View, 
    colors,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO

def main(page: Page):
    page.title = "Routes Example"

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

    page.add(
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
    )

    def route_change(e):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Flet app"), bgcolor=colors.INDIGO),
                    ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
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
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                View(
                    "/store",
                    [
                        AppBar(title=Text("Store"), bgcolor=colors.INDIGO),
                        ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


flet.app(main)