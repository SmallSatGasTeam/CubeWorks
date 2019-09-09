from Components.Component import Component


class ContextPrinter(Component):
    def __init__(self):
        super().__init__("ContextPrinter", 1)

    def update(self, context):
        print(context)
