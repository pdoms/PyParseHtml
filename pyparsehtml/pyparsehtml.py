from src import parse_doc_string, getters
from src.element import Element

class HtmlParser:
    def __init__(self, htmlstring):
        self.htmlstring = htmlstring
        (self.sequence, self.elements) = parse_doc_string.mapHTMLString(self.htmlstring)
  
    
    def document(self):
        pass

    def DOM(self):
        elementlist = []
        for element in self.elements:
             elementlist.append(vars(element))
        return elementlist
    
    def getElementById(self, id): 
        return getters.getBy_Element(id, self.elements)
    

"""






    #watch out what happens after overwrites like content of an element
    # thus, find a way to constantly update the list of elements 

 def getElementById(self, id, asString=False):
        element = helpers.getElement_byId(id, self.elements)
        if element == None:
            return None
        if asString:
            return helpers.representElementAsString(element)
        else: 
            return element




    def getElementsByTag(self, tag, asString=False):
        elements = helpers.getElements_byTag(tag, self.elements)
        asStrings = []  
        if elements == []:
            return []      
        if asString:
            for element in elements:
                asStrings.append(helpers.representElementAsString(element))
            return asStrings
        else: 
            return elements




    def getElementsByClass(self, className, asString=False):
        elements = helpers.getElements_byClass(className, self.elements)
        asStrings = []
        if elements == []:
            return []
        if asString: 
            for element in elements:
                asStrings.append(helpers.representElementAsString(element))
            return asStrings
        else:
            return elements
    

    def createElement(self, type):
        return helpers.create_Element(type)



    def appendChild(self, child):
        #to do this, I need to set up a way 
        # that indicates parent child relations
        # which in turn gives way for parent or child methods like: removeChildren/removeChild
        pass
    
    def insertElementAt(self, element):
        #at what?
        pass

    def cloneElement(self, element):
        return helpers.clone_Element( element)

    def removeElement(self, element):
        pass

    def removeAllElementsOf(self, identifier):
        pass

    def returnAsHTML(self):
        #will return up-to-date string 
        pass
    def saveAsHTML(self):
        pass
 """
teststring = '<div id="testID" class="testdivone">Hello<div class="testdivtwo">What <div id="childdiv">IS ACTUALLY</div> up?</div><div class="testdiv">S</div><img class="testimage"/><div style="color: green; width: 20px; height: 50cm;" /></div>'

test = HtmlParser(teststring)








    









