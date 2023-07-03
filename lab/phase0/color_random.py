from coloraide import Color
import flet as ft


class ColorButtons(ft.UserControl):
    def __init__(self, theme_function, **kwargs):
        super().__init__(**kwargs)
        self.callback = theme_function

    def build(self):
        return ft.Column(
            [
                ft.FilledTonalButton("RANDOM COLOR", on_click=self.random_color),
                ft.FilledTonalButton("RESET COLOR", on_click=self.reset_color),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def random_color(self, e):
        random_hex = Color.random("srgb").to_string(hex=True, upper=True)
        self.callback(random_hex)

    def reset_color(self, e):
        self.callback()


def main(page: ft.Page):
    def set_color(color: str = "#b2a2c1"):
        page.theme = ft.Theme(color_scheme_seed=color)
        page.update()

    def set_dark(e):
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.LIGHT if is_dark else ft.ThemeMode.DARK
        dark_button.icon = ft.icons.WB_SUNNY_OUTLINED if is_dark else ft.icons.WB_SUNNY
        page.update()

    page.title = "Theme Randomizer"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    dark_button = ft.IconButton(icon=ft.icons.WB_SUNNY, on_click=set_dark)

    page.add(
        *[
            ColorButtons(set_color),
            dark_button,
        ]
    )


if __name__ == "__main__":
    ft.app(target=main)
