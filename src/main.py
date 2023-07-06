from typing import List

import flet as ft

from chrocolor import ChroColor
from colorpicker import ColorPicker
from setting import Setting


class ChromatApp(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        self.page: ft.Page = page
        super().__init__(**kwargs)

        self.settings = [Setting(self, "test", ChroColor("#30ee90"), False)]
        self.picker = ColorPicker(self.settings[0])

        self.picker_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=self.picker,
            actions=[
                ft.TextButton("cancel", on_click=self.close_picker),
                ft.TextButton("save", on_click=self.save_color),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def build(self):
        return ft.ResponsiveRow(
            [
                ft.Column(
                    controls=self.settings,  # type: ignore
                    col=10,
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def open_picker(self, setting: Setting):
        self.picker = ColorPicker(setting)
        self.picker_dlg.content = self.picker
        self.page.dialog = self.picker_dlg
        self.picker_dlg.open = True
        self.page.update()

    def close_picker(self, e):
        self.picker_dlg.open = False
        self.page.update()

    def save_color(self, e):
        self.picker.write()
        self.close_picker(e)


def main(page: ft.Page):
    def toggle_dark(e):
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.LIGHT if is_dark else ft.ThemeMode.DARK
        dark_button.icon = ft.icons.WB_SUNNY_OUTLINED if is_dark else ft.icons.WB_SUNNY
        page.update()

    page.title = "chromat"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    page.fonts = {
        "Space Mono": "fonts/SpaceMono-Regular.ttf",
    }

    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.PURPLE_500, font_family="Space Mono"
    )

    dark_button = ft.IconButton(icon=ft.icons.WB_SUNNY, on_click=toggle_dark)

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=69,
        title=ft.Text(
            "chromat",
            font_family="Space Mono",
            weight=ft.FontWeight.BOLD,
        ),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            dark_button,
        ],
    )

    app = ChromatApp(page)
    page.add(app)


ft.app(main, assets_dir="../assets")
