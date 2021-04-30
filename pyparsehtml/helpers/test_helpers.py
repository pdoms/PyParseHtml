import unittest
import helpers_parse_initial as helpers
import helpers_getters as getters



#for has closing tag only use the parts of which the key is checked
has_closing_input_1 = [{'tag_role': 'open'}, {'tag_role': 'self_closing'}, {'tag_role': 'close'}]
has_closing_input_2 = [{'tag_role': 'open'}, {'tag_role': 'open'}, {'tag_role': 'open'}]
elements_forId = [{'id': '1'}, {'id': '2'}, {'id': '3'}]
elements_forTag = [{'tag_type': 'div'}, {'tag_type': 'img'}, {'tag_type': 'div'}]
elements_forClass = [{'class': 'class1'}, {'class': 'class2'}, {'class': 'class2'}]

test_input_string = '<div id="test1" style="text-align:left;" >Hello</div><img src="example.com" />'



test_data_div_for = {'tag_type': 'div', 'start_idx': 0, 'end_idx': 41, 'with_attributes': '<div id="test1" style="text-align:left;" >', 'as_tag_identifier': '<div>', 'tag_role': 'open', 'allowed_attributes': {'accesskey': '', 'class': '', 'contenteditable': '', 'data-*': '', 'dir': '', 'draggable': '', 'hidden': '', 'id': 'test1', 'lang': '', 'onblur': '', 'onchange': '', 'onclick': '', 'oncontextmenu': '', 'oncopy': '', 'oncut': '', 'ondblclick': '', 'ondrag': '', 'ondragend': '', 'ondragenter': '', 'ondragleave': '', 'ondragover': '', 'ondragstart': '', 'ondrop': '', 'onfocus': '', 'oninput': '', 'oninvalid': '', 'onkeydown': '', 'onkeypress': '', 'onkeyup': '', 'onmousedown': '', 'onmousemove': '', 'onmouseout': '', 'onmouseover': '', 'onmouseup': '', 'onmousewheel': '', 'onpaste': '', 'onscroll': '', 'onselect': '', 'onwheel': '', 'spellcheck': '', 'style': {'align-content': '', 'align-items': '', 'align-self': '', 'animation': '', 'animation-delay': '', 'animation-direction': '', 'animation-duration': '', 'animation-fill-mode': '', 'animation-iteration-count': '', 'animation-name': '', '@keyframes': '', 'animation-play-state': '', 'animation-timing-function': '', 'backface-visibility': '', 'background': '', 'background-attachment': '', 'background-clip': '', 'background-color': '', 'background-image': '', 'background-origin': '', 'background-position': '', 'background-repeat': '', 'background-size': '', 'border': '', 'border-bottom': '', 'border-bottom-color': '', 'border-bottom-left-radius': '', 'border-bottom-right-radius': '', 'border-bottom-style': '', 'border-bottom-width': '', 'border-collapse': '', 'border-color': '', 'border-image': '', 'border-image-outset': '', 'border-image-repeat': '', 'border-image-slice': '', 'border-image-source': '', 'border-image-width': '', 'border-left': '', 'border-left-color': '', 'border-left-style': '', 'border-left-width': '', 'border-radius': '', 'border-right': '', 'border-right-color': '', 'border-right-style': '', 'border-right-width': '', 'border-spacing': '', 'border-style': '', 'border-top': '', 'border-top-color': '', 'border-top-left-radius': '', 'border-top-right-radius': '', 'border-top-style': '', 'border-top-width': '', 'border-width': '', 'bottom': '', 'box-shadow': '', 'box-sizing': '', 'caption-side': '', 'clear': '', 'clip': '', 'color': '', 'column-count': '', 'column-fill': '', 'column-gap': '', 'column-rule': '', 'column-rule-color': '', 'column-rule-style': '', 'column-rule-width': '', 'column-span': '', 'column-width': '', 'columns': '', 'content': '', 'counter-increment': '', 'counter-reset': '', 'cursor': '', 'direction': '', 'display': '', 'empty-cells': '', 'flex': '', 'flex-basis': '', 'flex-direction': '', 'flex-flow': '', 'flex-wrap': '', 'flex-grow': '', 'flex-shrink': '', 'float': '', 'font': '', 'font-family': '', 'font-size': '', 'font-size-adjust': '', 'font-stretch': '', 'font-style': '', 'font-variant': '', 'font-weight': '', 'height': '', 'justify-content': '', 'left': '', 'letter-spacing': '', 'line-height': '', 'list-style': '', 'list-style-image': '', 'list-style-position': '', 'list-style-type': '', 'margin': '', 'margin-bottom': '', 'margin-left': '', 'margin-right': '', 'margin-top': '', 'max-height': '', 'max-width': '', 'min-height': '', 'min-width': '', 'opacity': '', 'order': '', 'outline': '', 'outline-color': '', 'outline-offset': '', 'outline-style': '', 'outline-width': '', 'overflow': '', 'overflow-x': '', 'overflow-y': '', 'padding': '', 'padding-bottom': '', 'padding-left': '', 'padding-right': '', 'padding-top': '', 'page-break-after': '', 'page-break-before': '', 'page-break-inside': '', 'perspective': '', 'perspective-origin': '', 'position': '', 'quotes': '', 'resize': '', 'right': '', 'tab-size': '', 'table-layout': '', 'text-align': 'left', 'text-align-last': '', 'justify': '', 'text-decoration': '', 'text-decoration-color': '', 'text-decoration-line': '', 'text-decoration-style': '', 'text-indent': '', 'text-justify': '', 'text-overflow': '', 'text-shadow': '', 'text-transform': '', 'top': '', 'transform': '', 'transform-origin': '', 'transform-style': '', 'transition': '', 'transition-delay': '', 'transition-duration': '', 'transition-property': '', 'transition-timing-function': '', 'vertical-align': '', 'visibility': '', 'white-space': '', 'width': '', 'word-break': '', 'word-spacing': '', 'word-wrap': '', 'z-index': ''}, 'tabindex': '', 'title': '', 'translate': ''}, 'seq_id': '0-1_div', 'closer': {'tag_type': 'div', 'tag_role': 'close', 'as_tag_identifier': '<div>', 'start_idx': 47, 'end_idx': 52, 'with_attributes': "", 'seq_id': '0-2_div'}, 'innerContent': 'Hello'}






class TestHelpers_parse_initial(unittest.TestCase):
    def test_mergeDict(self):
        """
        Test that dictionaries get concatetnated to one. 
        """
        data = [{"a": 1}, {"b": 2}, {"c": 3}, {"d": 4}]
        result = helpers.mergeDict(data)
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3, "d": 4})
    
    def test_isSelfCloserPos(self):
        """
        Test that tag is one that closes self.
        """
        
        positive_data = '<img>'

        result1 = helpers.isSelfCloser(positive_data)
   
        self.assertTrue(result1)
 
    
    def test_isSelfCloserNeg(self):
        """
        Test that tag is not one that closes self.
        """
        negative_data = '</div>'
        result2 = helpers.isSelfCloser(negative_data)
        self.assertFalse(result2)
    
    def test_hasClosingTagsPos(self):
        """test if list has closing tag"""
        data = helpers.hasClosingTags(has_closing_input_1)
        self.assertTrue(data)

    def test_hasClosingTagsNeg(self):
        """test if list has no closing tag"""
        data = helpers.hasClosingTags(has_closing_input_2)
        self.assertFalse(data)

    def test_tagToString(self):
        """test how the tag translates to a string"""
        par = getters.representElementAsString(test_data_div_for)
        expectedResult = '<div id="test1" style="text-align:left;" >Hello</div>'
        self.assertEqual(par, expectedResult)



    def test_getElementByID(self):
        """test if correct element is fetched using ID"""
        res = getters.getElement_byId('2', elements_forId)
        self.assertEqual(res, {'id': '2'})
    
    def test_getElementByID_negative(self):
        """test if None is returned when param doesn't match any id"""
        res = getters.getElement_byId('4', elements_forId)
        self.assertIsNone(res)
    
    def test_getElementsByTag(self):
        """test if collection of elements is returned by matching tags"""
        result = getters.getElements_byTag('div', elements_forTag)
        self.assertEqual(result, [{'tag_type': 'div'},{'tag_type': 'div'}])
    
    def test_getElementsByTag_negative(self):
        """test if empty list is returned when none match"""
        result = getters.getElements_byTag('input', elements_forTag)
        self.assertEqual(result, [])

    def test_getElementsByClass(self):
        """test if collection of elements is returned by matching class names"""
        result = getters.getElements_byClass('class2', elements_forClass)
        self.assertEqual(result, [{'class': 'class2'},{'class': 'class2'}])
    
    def test_getElementsByClass_negative(self):
        """test if None is returned when param doesn't match any class"""
        result = getters.getElements_byClass('class4', elements_forClass)
        self.assertEqual(result, [])
    

 
if __name__ == '__main__':
    unittest.main()

