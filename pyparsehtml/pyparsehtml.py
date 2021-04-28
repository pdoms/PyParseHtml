import helpers

class HTMLParser:
    def __init__(self, htmlstring):
        self.htmlstring = htmlstring
        (self.sequence, self.elements) = helpers.mapHTMLString(self.htmlstring)
        
    def __repr__(self):
        return str(self.elements)

    ## returns all elements found in the initial string or in the current
    ## state of the document 
    def getParsedHtml(self, rep):
        #don't forget to handle the updates when it's time
        (seq, ele) = helpers.mapHTMLString(self.htmlstring)
        self.elements = ele
        self.sequence = seq
        if rep == 'tags':
            return self.elements
        else: 
            return self.sequence







    #watch out what happens after overwrites like content of an element
    # thus, find a way to constantly update the list of elements 

    def getElementById(self, id, asString=False):
        element = helpers.getElement_byId(id, self.elements)
        if asString:
            return helpers.representElementAsString(element)
        else: 
            return element

    def getElementsByTag(self, tag):
        pass
    def getElementsByClass(self, className):
        #maybe lift id/class to upper nesting
        pass
    
    def createElement(self, type):
        pass

    def appendChild(self, child):
        #to do this, I need to set up a way 
        # that indicates parent child relations
        # which in turn gives way for parent or child methods like: removeChildren/removeChild
        pass
    
    def insertElementAt(self, element):
        #at what?
        pass

    def removeElement(self, element):
        pass

    def removeAllElementsOf(self, identifier):
        pass

    def returnAsHTML(self):
        #will return up-to-date string 
        pass
    def saveAsHTML(self):
        pass

teststring = '<div id="testID" class="testdivone">Hello<div class="testdivtwo">What up?</div><div class="testdiv">S</div><img class="testimage"/><div style="color: green; width: 20px; height: 50cm;" /></div>'

test = HTMLParser(teststring)
byId = test.getElementById("testID", asString=False)
print(byId)