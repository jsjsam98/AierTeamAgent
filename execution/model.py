class Rect:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class ItemDetail:
    def __init__(self, name: str, type: str, rect: Rect):
        self.name = name
        self.type = type
        self.rect = rect


class ItemBrief:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type
