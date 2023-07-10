import flet as ft


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
            "/img/chromat_white.png"
            if page.theme_mode == ft.ThemeMode.DARK
            else "/img/chromat_black.png"
        )
        return ft.Container(
            content=ft.Image(src=img_path, fit=ft.ImageFit.CONTAIN, height=64),
            padding=8,
        )

    page.appbar = ft.AppBar(
        leading=app_logo(),
        leading_width=300,
        bgcolor=ft.colors.SURFACE_VARIANT,
        toolbar_height=72,
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
            ft.Text("haha Yeet"),
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="..\assets")
