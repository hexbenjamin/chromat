import flet as ft


class Panel(ft.Container):
    def __init__(self, operator, **kwargs):
        self.operator = operator
        super().__init__(**kwargs)

    def send(self, target, property_name, message):
        self.operator.broadcast(self, target, property_name, message)

    def receive(self, sender, property_name, message):
        setattr(self, property_name, message)
        self.update()


class PickerPanel(Panel):
    def __init__(self, operator, **kwargs):
        self.hue_slider = self.make_slider("H", 360, "°")
        self.sat_slider = self.make_slider("S", 100, "%")
        self.lum_slider = self.make_slider("L", 100, "%")

        super().__init__(
            operator,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        self.make_swatch(),
                        self.make_sliders_panel(),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            bgcolor=ft.colors.SURFACE,
            alignment=ft.alignment.center,
            padding=8,
            **kwargs,
        )

    def make_slider(self, label: str, max: int, symbol: str):
        return ft.Slider(
            min=0,
            max=max,
            divisions=max,
            label=f"{{value}}{symbol}",
            expand=True,
        )

    def make_swatch(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Card(
                        content=ft.Container(
                            content=ft.Text("#XXXXXX", size=21),
                            alignment=ft.alignment.bottom_left,
                            padding=ft.Padding(8, 16, 24, 8),
                        )
                    )
                ]
            ),
        )

    def make_sliders_panel(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Text(
                                "H",
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.ON_SURFACE,
                            ),
                            self.hue_slider,
                        ],
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                "S",
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.ON_SURFACE,
                            ),
                            self.sat_slider,
                        ],
                    ),
                    ft.Row(
                        [
                            ft.Text(
                                "L",
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.ON_SURFACE,
                            ),
                            self.lum_slider,
                        ],
                    ),
                ],
            ),
            padding=12,
        )

    @property
    def swatch(self):
        hue = self.hue_slider.value
        sat = self.sat_slider.value
        lum = self.lum_slider.value
