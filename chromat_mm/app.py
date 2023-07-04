from typing import Literal, Callable

import flet as ft

from .util import ChroColor
from .widgets import ColorPicker


INIT_SWATCH = ChroColor("lch", [50.0, 75.0, 180.0])


def main(page: ft.Page):
    def toggle_dark(e):
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.LIGHT if is_dark else ft.ThemeMode.DARK
        dark_button.icon = ft.icons.WB_SUNNY_OUTLINED if is_dark else ft.icons.WB_SUNNY
        page.update()

    def bs_dismissed(e):
        # print("Dismissed!")
        pass

    def show_picker(e):
        bs.open = True
        bs.update()

    def picker_selected(e):
        page.theme = ft.Theme(color_scheme_seed=picker.swatch.hex)
        bs.open = False
        bs.update()
        page.update()

    page.title = "chromat"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.window_width = 700
    # page.window_height = 500
    # page.window_min_width = 700
    # page.window_min_height = 500
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed=INIT_SWATCH.hex)

    dark_button = ft.IconButton(icon=ft.icons.WB_SUNNY, on_click=toggle_dark)

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=69,
        title=ft.Text("chromat : HCL Picker"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            dark_button,
        ],
    )

    picker = ColorPicker(INIT_SWATCH)

    # page.add(layout)

    bs = ft.BottomSheet(
        ft.Container(
            content=ft.Column(
                [
                    picker,
                    ft.FilledTonalButton("[ select ]", on_click=picker_selected),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            padding=ft.Padding(16, 0, 16, 0),
        ),
        open=False,
        on_dismiss=bs_dismissed,
    )
    page.overlay.append(bs)
    page.add(ft.FilledButton("pick a color!", on_click=show_picker))


if __name__ == "__main__":
    ft.app(target=main)
