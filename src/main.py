from typing import List

import flet as ft

from chrocolor import ChroColor
from colorpicker import ColorPicker
from database import get_picker_settings
from setting import Setting


class ChromatApp(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        self.page: ft.Page = page
        super().__init__(**kwargs)

        self.settings = [
            Setting(
                app=self,
                parameter=setting["parameter"],
                default_color=ChroColor(
                    "srgb",
                    [
                        setting["value"]["red"] / 255,
                        setting["value"]["green"] / 255,
                        setting["value"]["blue"] / 255,
                    ],
                ),
                optional=setting["optional"],
            )
            for setting in get_picker_settings("general")
        ]

        self.picker = ColorPicker(Setting(self, "temp", ChroColor("#000000"), False))

        self.picker_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("edit color"),
            content=self.picker,
            actions=[
                ft.TextButton("cancel", on_click=self.close_picker),
                ft.TextButton("save", on_click=self.save_color),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def build(self):
        return ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            ft.ListView(
                                controls=self.settings,  # type: ignore
                                expand=1,
                                spacing=10,
                                padding=20,
                                auto_scroll=True,
                            ),
                        ],
                        col={"xs": 12, "sm": 10, "md": 8, "lg": 6, "xl": 6},
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
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
    page.add(
        ft.SafeArea(
            app,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(main, assets_dir="../assets")
