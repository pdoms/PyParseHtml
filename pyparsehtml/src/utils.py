
from .html_data import html_tags_incl_attributes, global_attributes, css_properties, self_closer
import copy


def seqIdtoDict(id):
  return {
      'seq_id': id,
      'seq_tag_type': id[id.index('_')+1:],
      'seq_unique': id[:id.index('-')],
      'seq_tag_role': id[id.index('-')+1: id.index('_')] 
  }




def printElement(element):
    if element.tag_role == 'open_close' or element.tag_role == 'open_close_alt':
        return element.with_attributes
    return f"{element.with_attributes}{element.innerHTML}</{element.closer['tag_type']}>"


            

        
 

def representElementAsString(tag):
    if tag['tag_role'] == 'open_close' or tag['tag_role'] == 'open_close_alt':
        return tag['with_attributes']
    else: 
        return f"{tag['with_attributes']}{tag['innerHTML']}</{tag['closer']['tag_type']}>"

def mergeDict(dictionaries):
  base = dictionaries[0]
  for d in range(1, len(dictionaries)):
    base.update(dictionaries[d])
  return base

def isSelfCloser(to_match):
  res = False
  for o in self_closer:
    if to_match == o[0] or to_match == o[1]:
      res = True
  return res


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

def getTagBySeqId(tags, seq_id):
    s = seqIdtoDict(seq_id)
    if s['seq_tag_role'] == '1' or s['seq_tag_role'] == '3':
        for t in tags:
            if s['seq_id'] == t['seq_id']:
                return t
    else:
        for t in tags: 
            if 'closer' in t:
                if s['seq_id'] == t['closer']['seq_id']:
                    return t['closer']




    


