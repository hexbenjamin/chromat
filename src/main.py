import flet as ft


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

PANELS = []


# + PANELS DECORATOR FUNCTION
def store_panel(function):
    def wrapper(*args, **kwargs):
        ref = function(*args, **kwargs)
        PANELS.append(ref)
        return ref

    return wrapper


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
        color_scheme_seed=ft.colors.PURPLE_500, font_family="Space Mono"
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

    main_column = ft.Column(
        controls=[ft.Text("haha Yeet !")],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page.add(
        ft.SafeArea(
            main_column,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="..\\assets")
