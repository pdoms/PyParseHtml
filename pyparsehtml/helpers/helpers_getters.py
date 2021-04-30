def representElementAsString(tag):
    if tag['tag_role'] == 'open_close' or tag['tag_role'] == 'open_close_alt':
        return tag['with_attributes']
    else: 
        return f"{tag['with_attributes']}{tag['innerContent']}</{tag['closer']['tag_type']}>"


def getElement_byId(id, tags):
    return_value = None
#will always return the first element found because ids should be unique anyways
    for tag in tags:
        if tag['id'] == id:
            return_value = tag
    return return_value

def getElements_byTag(tag_name, tags):
    collected = []
    for tag in tags:
        if tag['tag_type'] == tag_name:
            collected.append(tag)
    return collected

def getElements_byClass(class_name, tags):
    collected = []
    for tag in tags:
        if tag['class'] == class_name:
            collected.append(tag)
    return collected
