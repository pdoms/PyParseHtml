def representElementAsString(tag):
    print(type(tag))
    if tag['tag_role'] == 'open_close' or tag['tag_role'] == 'open_close_alt':
        return tag['with_attributes']
    else: 
        return f"{tag['with_attributes']}{tag['innerContent']}</{tag['closer']['tag_type']}>"


def getElement_byId(id, tags):
#will always return the first element found because ids should be unique anyways
    for tag in tags:
        if tag['allowed_attributes']['id'] == id:
            return tag


