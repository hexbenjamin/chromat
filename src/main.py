import flet as ft

from chrocolor import ChroColor


class Setting(ft.Card):
    def __init__(
        self,
        page: ft.Page,
        parameter: str,
        default_color: ChroColor,
        optional: bool,
        **kwargs,
    ):
        self.page: ft.Page = page
        self.parameter = parameter
        self.optional = optional
        self.swatch = default_color

        self.container = ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            ft.Icon(
                                ft.icons.STARS_ROUNDED,
                                color=ft.colors.SURFACE_VARIANT
                                if self.optional
                                else ft.colors.GREEN_600,
                            ),
                        ],
                        col=1,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Column(
                        [
                            ft.Text(self.parameter),
                        ],
                        col=4,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Column(
                        [
                            ft.Text(self.swatch.hex),
                            ft.Text(", ".join([str(x) for x in self.swatch.rgb])),
                        ],
                        col=4,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    ft.Column(
                        [
                            ft.FilledButton(
                                "edit",
                                icon=ft.icons.EDIT,
                                on_click=self.edit_clicked,
                            ),
                        ],
                        col=3,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding(12, 8, 12, 8),
        )

        super().__init__(content=self.container, **kwargs)

    def edit_clicked(self, e):
        self.make_theme()
        self.swatch.update(ChroColor.random("srgb"))

    def make_theme(self):
        self.theme = ft.Theme(primary_swatch=self.swatch.hex, font_family="Space Mono")
        self.container.theme = self.theme
        self.page.update()


class ChromatApp(ft.UserControl):
    def __init__(self, page: ft.Page, **kwargs):
        self.page: ft.Page = page
        super().__init__(**kwargs)

    def build(self):
        return Setting(self.page, "test", ChroColor("#30ee90"), False)


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

    page.add(ChromatApp(page))


ft.app(main, assets_dir="../assets")
