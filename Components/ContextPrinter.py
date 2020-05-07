from Components.Component import Component


class ContextPrinter(Component):
    """
    Concrete child of the Component class.
    collects context as an argument and prints it to the terminal
    """
    def __init__(self):
        """
        Initializes a ContextPrinter object.  Calls the parent constructor.
        """
        super().__init__("ContextPrinter", 1)

    def update(self, context):
        """
        Concrete method defining the abstract Component.update() method.  Prints context to the terminal.
        """
        print(context)
