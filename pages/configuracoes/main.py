from flet import(
    Column,
    Row,
    ElevatedButton,
    icons,
    FilePicker,
    FilePickerResultEvent,
    Text,
    Page,
    FilePickerUploadFile,
)

import navigation
import services.config as sv_config

page = Page

# Pick files dialog
def pick_files_result(e: FilePickerResultEvent):
    selected_files.value = (
        ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
    )
    selected_files.update()

    #upload_list = []

    #for file in e.files:
    #    upload_list.append(
    #        FilePickerUploadFile(
    #            file.name,
    #            upload_url=page.get_upload_url(file.name, 600),
    #        )
    #    )

    #pick_files_dialog.upload(upload_list)

    #print("content")
    #tela.controls[4].value = "content"
    
    #navigation.refresh()

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

def upload_files(e):
    upload_list = []
    if pick_files_dialog.result != None and pick_files_dialog.result.files != None:
        for f in pick_files_dialog.result.files:
            upload_list.append(
                FilePickerUploadFile(
                    f.name,
                    upload_url=page.get_upload_url(f.name, 600),
                )
            )
        pick_files_dialog.upload(upload_list)


# hide all dialogs in overlay
#page.overlay.extend([pick_files_dialog, save_file_dialog, get_directory_dialog])

tela = Column(
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
        Row(
            [
                ElevatedButton(
                    "Upload file",
                    icon=icons.FOLDER_OPEN,
                    on_click=upload_files,
                ),
            ]
        ),
        Text("")
    ],
    visible=False
)

def on_visible():
    pass

navigation.paginas.append(
    {
        'objeto': tela,
        'numero': '20',
        'vis_event': on_visible,
        'titulo': f"{sv_config.get('versao')} - Configurações",
    }
)