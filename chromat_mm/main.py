from typing import Literal, Callable
from .chrocolor import ChroColor

import flet as ft

SWATCH = ChroColor("lch", [50.0, 75.0, 180.0])


class SwatchDisplay(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.text = ft.Text(
            SWATCH.hex,
            color=SWATCH.accent.hex,
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            text_align=ft.TextAlign.RIGHT,
        )
        self.card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        self.text,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                ),
                padding=27,
            ),
            width=420,
            color=SWATCH.hex,
        )

        return self.card

    def update_color(self):
        self.text.value = SWATCH.hex
        self.text.color = SWATCH.accent.hex
        self.card.color = SWATCH.hex
        self.update()


class HCLSlider(ft.UserControl):
    def __init__(
        self,
        mode: Literal["H", "C", "L"],
        update: Callable,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.mode = mode
        self._vals = {
            "H": {
                "full": "hue",
                "max": 360,
                "label": "{value}º",
            },
            "C": {
                "full": "chroma",
                "max": 150,
                "label": "{value}",
            },
            "L": {
                "full": "luminance",
                "max": 100,
                "label": "{value}%",
            },
        }
        self.update_swatch = update

    def build(self):
        self.mode_obj = self._vals[self.mode]

        self.slider = ft.Slider(
            min=0,
            max=self.mode_obj["max"],
            divisions=self.mode_obj["max"],
            label=self.mode_obj["label"],
            on_change=self.on_slider_change,
        )

        self.slider.value = self.mode_obj["max"] / 2

        return ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        [ft.Text(self.mode, text_align=ft.TextAlign.RIGHT, size=24)],
                        col=1,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Column(
                        [self.slider],
                        col=11,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(32, 8, 32, 8),
        )

    def on_slider_change(self, e):
        lch = SWATCH.convert("lch").to_dict()
        lch["coords"][["L", "C", "H"].index(self.mode)] = e.control.value
        SWATCH.update(ChroColor(lch))
        self.update_swatch()


class SliderPanel(ft.UserControl):
    def __init__(self, update: Callable, **kwargs):
        super().__init__(**kwargs)
        self.update_swatch = update

    def build(self):
        return ft.Card(
            content=ft.Column(
                [
                    HCLSlider(mode="H", update=self.update_swatch),
                    HCLSlider(mode="C", update=self.update_swatch),
                    HCLSlider(mode="L", update=self.update_swatch),
                ],
            ),
        )


class ConvertPanel(ft.UserControl):
    def __init__(self, mode: str = "rgb", **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return None


def main(page: ft.Page):
    def toggle_dark(e):
        is_dark = page.theme_mode == ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.LIGHT if is_dark else ft.ThemeMode.DARK
        dark_button.icon = ft.icons.WB_SUNNY_OUTLINED if is_dark else ft.icons.WB_SUNNY
        page.update()

    def update_swatch():
        swatch_display.update_color()
        page.theme = ft.Theme(color_scheme_seed=SWATCH.hex)
        page.update()

    page.title = "Theme Randomizer"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 700
    page.window_height = 500
    page.window_min_width = 700
    page.window_min_height = 500
    page.theme_mode = ft.ThemeMode.DARK

    dark_button = ft.IconButton(icon=ft.icons.WB_SUNNY, on_click=toggle_dark)

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=69,
        title=ft.Text("HCL Picker"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            dark_button,
        ],
    )

    swatch_display = SwatchDisplay()

    layout = ft.Container(
        content=ft.Column(
            [
                swatch_display,
                SliderPanel(update=update_swatch),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.Padding(32, 16, 32, 16),
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)
