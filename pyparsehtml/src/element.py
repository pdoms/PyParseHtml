from src.utils import printElement

#the class attributes should be filtered for the user, not all are relevant


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
        