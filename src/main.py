from typing import Optional

import flet as ft

from connector import Operator
from panels import Panel, PickerPanel


"""
from random import choice

COLORS = [
    ft.colors.RED,
    ft.colors.DEEP_ORANGE,
    ft.colors.ORANGE,
    ft.colors.AMBER,
    ft.colors.YELLOW,
    ft.colors.LIME,
    ft.colors.LIGHT_GREEN,
    ft.colors.GREEN,
    ft.colors.TEAL,
    ft.colors.CYAN,
    ft.colors.LIGHT_BLUE,
    ft.colors.BLUE,
    ft.colors.INDIGO,
    ft.colors.DEEP_PURPLE,
    ft.colors.PURPLE,
    ft.colors.PINK,
]
"""

OPERATOR = Operator()


# + PANELS DECORATOR FUNCTION
def register(name: str):
    def wrapper(func):
        def func_wrapper(*args, **kwargs):
            ref = func(*args, **kwargs)
            OPERATOR.register(ref, name)
            return ref

        return func_wrapper

    return wrapper


# + APP CLASS
class ChromatApp(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self.make_settings_panel(),
                        self.make_io_panel(),
                    ],
                    expand=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        self.make_picker_panel(),
                        self.make_modes_panel(),
                    ],
                    expand=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
        )

    # - PANELS

    @register("settings")
    def make_settings_panel(self):
        return Panel(
            OPERATOR,
            content=ft.Text("SettingsPanel", weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.RED_200,
            expand=3,
            alignment=ft.alignment.center,
        )

    @register("picker")
    def make_picker_panel(self):
        return PickerPanel(OPERATOR, expand=3)

    @register("modes")
    def make_modes_panel(self):
        return Panel(
            OPERATOR,
            content=ft.Text("ModesPanel", weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.LIGHT_BLUE_200,
            expand=5,
            alignment=ft.alignment.center,
        )

    @register("io")
    def make_io_panel(self):
        return Panel(
            OPERATOR,
            content=ft.Text("IOPanel", weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.PURPLE_200,
            expand=1,
            alignment=ft.alignment.center,
        )


# + APP FUNCTION
def main(page: ft.Page):
    page.title = "chromat"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    page.fonts = {
        "Space Mono": "fonts/SpaceMono-Regular.ttf",
    }

    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.PURPLE_500,
        font_family="Space Mono",
    )

    def app_logo():
        img_path = (
            "/img/chromat_light.png"
            if page.theme_mode == ft.ThemeMode.DARK
            else "/img/chromat_dark.png"
        )
        blend_mode = (
            ft.BlendMode.MULTIPLY
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.BlendMode.SOFT_LIGHT
        )

        return ft.Container(
            content=ft.Container(
                content=ft.Image(
                    src=img_path,
                    color=ft.colors.PRIMARY,
                    color_blend_mode=blend_mode,
                    fit=ft.ImageFit.COVER,
                ),
                bgcolor=ft.colors.ON_SURFACE_VARIANT,
                border_radius=ft.border_radius.all(16),
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                height=44,
            ),
            padding=ft.Padding(8, 12, 8, 12),
        )

    page.appbar = ft.AppBar(
        leading=app_logo(),
        leading_width=200,
        bgcolor=ft.colors.SURFACE_VARIANT,
        toolbar_height=64,
    )

    def toggle_dark(e, app_bar: ft.AppBar = page.appbar):
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.LIGHT if is_dark else ft.ThemeMode.DARK
        app_bar.leading = app_logo()
        dark_button.icon = ft.icons.WB_SUNNY_OUTLINED if is_dark else ft.icons.WB_SUNNY
        page.update()

    dark_button = ft.IconButton(icon=ft.icons.WB_SUNNY, on_click=toggle_dark)

    page.appbar.actions = [
        ft.Container(
            content=dark_button,
            padding=8,
        )
    ]

    page.add(
        ft.SafeArea(
            ft.Container(
                content=ChromatApp(),
                padding=32,
            ),
            expand=True,
        ),
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="..\\assets")
