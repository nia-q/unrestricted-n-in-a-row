class Player:
    def __init__(self, name: str, symbol: str) -> None:
        self.name: str = name
        self.symbol: str = symbol

    def get_name(self) -> str:
        return self.name

    def get_symbol(self) -> str:
        return self.symbol
