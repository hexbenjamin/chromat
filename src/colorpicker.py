from typing import Any, Callable, Literal

import flet as ft

from ..util import ChroColor
from ..widgets.settingslist import SettingsRow


HCL_DICT = {
    "H": {
        "full": "hue",
        "max": 360,
        "label": "{value}º",
        "default": 180,
    },
    "C": {
        "full": "chroma",
        "max": 150,
        "label": "{value}",
        "default": 75,
    },
    "L": {
        "full": "luminance",
        "max": 100,
        "label": "{value}%",
        "default": 50,
    },
}


class ColorPicker(ft.UserControl):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.parent = parent
        self.swatch = ChroColor("#000000")
        self.caller: Any
        self.submit: Callable

    def build(self):
        self.display = SwatchDisplay(self.swatch)
        self.slider_panel = SliderPanel(parent=self)
        self.submit_button = ft.FilledButton("[ select ]", on_click=self.submit_called)

        return ft.Container(
            content=ft.Column(
                [
                    self.display,
                    self.slider_panel,
                    self.submit_button,
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(32, 16, 32, 16),
        )

    def update_swatch(self, swatch: ChroColor):
        self.swatch.update(swatch)
        self.display.swatch.update(swatch)
        self.display.update_color()
        self.update()

    def submit_called(self, e):
        self.submit(self.swatch)


class SwatchDisplay(ft.UserControl):
    def __init__(self, swatch: ChroColor, **kwargs):
        super().__init__(**kwargs)
        self.swatch = swatch

    def build(self):
        self.text = ft.Text(
            self.swatch.hex,
            color=self.swatch.accent.hex,
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
            width=270,
            color=self.swatch.hex,
        )

        return self.card

    def update_color(self):
        self.text.value = self.swatch.hex
        self.text.color = self.swatch.accent.hex
        self.card.color = self.swatch.hex
        self.update()


class SliderPanel(ft.UserControl):
    def __init__(self, parent: ColorPicker, **kwargs):
        super().__init__(**kwargs)
        self.parent = parent

    def build(self):
        self.h_slider = HCLSlider(parent=self, mode="H")
        self.c_slider = HCLSlider(parent=self, mode="C")
        self.l_slider = HCLSlider(parent=self, mode="L")
        return ft.Card(
            content=ft.Column(
                [
                    self.h_slider,
                    self.c_slider,
                    self.l_slider,
                ],
            ),
        )

    def update_swatch(self):
        l, c, h = self.l_slider.value, self.c_slider.value, self.h_slider.value
        self.parent.update_swatch(ChroColor("lch", [l, c, h]))


class HCLSlider(ft.UserControl):
    def __init__(
        self,
        parent: SliderPanel,
        mode: Literal["H", "C", "L"],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.parent = parent
        self.mode = mode
        self.value = HCL_DICT[self.mode]["default"]

    def build(self):
        self.mode_obj = HCL_DICT[self.mode]

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
            padding=ft.Padding(16, 8, 16, 8),
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=16,
        )

    def on_slider_change(self, e):
        # lch = INIT_SWATCH.convert("lch").to_dict()
        # lch["coords"][["L", "C", "H"].index(self.mode)] = e.control.value
        # INIT_SWATCH.update(ChroColor(lch))
        # self.update_swatch()
        self.value = e.control.value
        self.parent.update_swatch()
