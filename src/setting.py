import flet as ft

from chrocolor import ChroColor


class Setting(ft.UserControl):
    def __init__(
        self,
        app,
        parameter: str,
        default_color: ChroColor,
        optional: bool,
        **kwargs,
    ):
        self.app = app
        self.page: ft.Page = self.app.page
        self.parameter = parameter
        self.optional = optional
        self.swatch = default_color

        super().__init__(**kwargs)

    def build(self):
        self.theme: ft.Theme = self.make_theme()

        self.rgb_column = ft.Column(
            [
                RGBPanel(self),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.END,
            expand=True,
            col=8,
        )

        self.container = ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            ft.Icon(
                                ft.icons.STARS_ROUNDED,
                                color=ft.colors.SURFACE_VARIANT
                                if self.optional
                                else ft.colors.AMBER_300,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        expand=True,
                        col=4,
                    ),
                    ft.Column(
                        [
                            ft.Text(self.parameter, size=24),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        expand=True,
                        col=8,
                    ),
                    self.rgb_column,
                    ft.Column(
                        [
                            ft.ElevatedButton(
                                "edit",
                                icon=ft.icons.EDIT,
                                on_click=self.edit_clicked,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        expand=True,
                        col=4,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(12, 8, 12, 8),
            theme=self.theme,
        )

        return ft.Card(self.container, color=ft.colors.SURFACE_VARIANT)

    def edit_clicked(self, e):
        self.app.open_picker(self)

    def make_theme(self) -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=self.swatch.hex, on_primary=self.swatch.accent.hex
            ),
            font_family="Space Mono",
        )

    def update_color(self, color: ChroColor):
        self.swatch = color
        self.container.theme = self.make_theme()
        self.rgb_column.controls = [RGBPanel(self)]
        self.container.update()
        self.update()


class RGBPanel(ft.UserControl):
    def __init__(self, parent: Setting, **kwargs):
        self.parent = parent
        self.swatch = self.parent.swatch
        super().__init__(**kwargs)

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            self.swatch.hex,
                            color=self.swatch.accent.hex,
                            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                padding=ft.Padding(16, 8, 16, 8),
            ),
            color=self.swatch.hex,
            expand=True,
        )