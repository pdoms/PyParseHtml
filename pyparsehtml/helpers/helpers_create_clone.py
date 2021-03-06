from .helpers_parse_initial import mergeDict, html_tags_incl_attributes, global_attributes, isSelfCloser, css_properties, html_tags_stripped
import copy

def createBasics(type, isCloser=False):
    element = {}
    element['tag_type'] = type
    element['id'] = ""
    element['class'] = ""
    element['start_idx'] = ""
    element['end_idx'] = ""
    element['seq_id'] = ""
    if isCloser:
        element['tag_role'] = 'close'
        element['as_tag_identifier'] = f"<{type} />"
        element['with_attributes'] = ""
    return element


def appendGlobalAttributes(): 
    attributes = {}       
    for glob in global_attributes:
        if glob == 'style' or glob == 'id' or glob == 'class':
            continue
        else:
            attributes[glob] = ""
    return attributes

def appendSpecificAttributes(type):
    attributes = {}
    for tag in html_tags_incl_attributes:
        if f"<{type}>" == tag:
            for a in html_tags_incl_attributes[tag]:
                attributes[a] = ""
        if f"<{type} />" == tag:
            for a in html_tags_incl_attributes[tag]:
                attributes[a] = ""
    return attributes

def appendStyleProperties():
    properties = {}
    for prop in css_properties:
        properties[prop] = ""
    return properties
    
def create_Element(type):
    if type not in html_tags_stripped:
        return None
    element = createBasics(type)
    element['style'] = appendStyleProperties()
    if isSelfCloser(type):
        element['tag_role'] = 'open_close'
        element['as_tag_identifier'] = f"<{type} />"
        element['with_attributes'] = element['as_tag_identifier']
    else:
        element['tag_role'] = 'open'
        element['as_tag_identifier'] = f"<{type}>"
        element['closer'] = createBasics(type, True)
        element['with_attributes'] = element['as_tag_identifier']
        #create closer
    globals = appendGlobalAttributes()
    specific = appendSpecificAttributes(type)
    element['allowed_attributes'] = mergeDict([globals, specific])
    return element


def clone_Element(element):
    #what to do with inner contents and sequence?
    clone = copy.deepcopy(element)
    clone['seq_id'] = ""
    return clone






