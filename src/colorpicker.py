from typing import Literal

import flet as ft

from chrocolor import ChroColor
from setting import Setting


HCL_DICT = {
    "H": {
        "full": "hue",
        "max": 360,
        "label": "{value}º",
    },
    "S": {
        "full": "saturation",
        "max": 100,
        "label": "{value}%",
    },
    "L": {
        "full": "lightness",
        "max": 100,
        "label": "{value}%",
    },
}


class ColorPicker(ft.UserControl):
    def __init__(self, setting: Setting, **kwargs):
        super().__init__(**kwargs)
        self.setting = setting
        self.swatch = ChroColor(self.setting.swatch)

    def build(self):
        self.display = SwatchDisplay(self.swatch)
        self.slider_panel = SliderPanel(parent=self)

        return ft.Container(
            content=ft.Column(
                [
                    self.display,
                    self.slider_panel,
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
        self.setting.page.update()

    def write(self):
        self.setting.update_color(self.swatch)


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
            width=420,
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

        self.hue, self.saturation, self.lightness = self.parent.swatch.convert(
            "hsl"
        ).to_dict()["coords"]

        self.h_slider = HCLSlider(
            parent=self,
            mode="H",
            init_value=self.hue,
        )
        self.s_slider = HCLSlider(
            parent=self,
            mode="S",
            init_value=round(self.saturation * 100),
        )
        self.l_slider = HCLSlider(
            parent=self,
            mode="L",
            init_value=round(self.lightness * 100),
        )

    def build(self):
        return ft.Card(
            content=ft.Container(
                ft.Column(
                    [
                        self.h_slider,
                        self.s_slider,
                        self.l_slider,
                    ],
                ),
                padding=16,
            ),
        )

    def update_swatch(self):
        self.parent.update_swatch(self.swatch)

    @property
    def swatch(self) -> ChroColor:
        return ChroColor(
            "hsl",
            [self.h_slider.value, self.s_slider.value / 100, self.l_slider.value / 100],
        )

    @swatch.setter
    def swatch(self, value: ChroColor):
        self.hue, self.saturation, self.lightness = value.hsl


class HCLSlider(ft.UserControl):
    def __init__(
        self,
        parent: SliderPanel,
        mode: Literal["H", "S", "L"],
        init_value: float = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.parent = parent
        self.mode = mode
        self.value = init_value

    def build(self):
        self.mode_obj = HCL_DICT[self.mode]

        self.slider = ft.Slider(
            min=0,
            max=self.mode_obj["max"],
            divisions=self.mode_obj["max"],
            label=self.mode_obj["label"],
            on_change=self.on_slider_change,
        )

        self.slider.value = self.value

        return ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        [
                            ft.Text(
                                self.mode,
                                text_align=ft.TextAlign.RIGHT,
                                size=24,
                                style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                            )
                        ],
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
