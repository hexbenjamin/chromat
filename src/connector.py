class Operator:
    def __init__(self):
        self.panels = {}

    def register(self, panel, name: str):
        self.panels[name] = panel

    def unregister(self, name: str):
        self.panels.pop(name)

    def broadcast(self, sender, target, property_name, message):
        for name, panel in self.panels.items():
            if name == target:
                panel.receive(sender, property_name, message)
