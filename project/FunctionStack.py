class FunctionStack:
    def __init__(self, name):
        self.FunctionStack = []
        self.Name = name

    def AddFunction(self, Function, Arguments):
        self.FunctionStack.append([Function, Arguments])

    def Execute(self):
        self.FunctionStack[0][0](self.FunctionStack[0][1])
        self.FunctionStack.pop(0)
