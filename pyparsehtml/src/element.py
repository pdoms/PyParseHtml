from src.utils import printElement


class Element:
    def __init__(self, tag_set):
        for k, v in tag_set.items():
            setattr(self, k, v)
    def __str__(self) -> str:
        return printElement(self)

    
class lastChild:
    def __init__(self, tag_set):
        for k, v in tag_set.items():
            setattr(self, k, v)
        