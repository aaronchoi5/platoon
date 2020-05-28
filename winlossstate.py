class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
WinLossState = Enum(["WIN", "LOSS", "DRAW"])
print(WinLossState.WIN)