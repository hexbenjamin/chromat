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
