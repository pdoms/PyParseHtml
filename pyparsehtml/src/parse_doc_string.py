import re
import copy
from typing import Sequence
from .element import Element
from .utils import isSelfCloser, mergeDict, representElementAsString, seqIdtoDict
from .html_data import global_attributes, css_properties, html_tags_incl_attributes, html_tags_stripped

def addGlobalAttributes():
  attributes = {}
  for g in global_attributes:
    if g == 'style':
      attributes[g] = {}
      for prop in css_properties:
        attributes[g][prop] = ""
     
    else:
      attributes[g] = ""
  return attributes

def addSpecificAttributes(meta_tag):
  attributes = {}
  for a in html_tags_incl_attributes[meta_tag['as_tag_identifier']]:
    attributes[a] = ""
  return attributes

def sortTags(tags):
  return sorted(tags, key = lambda i: i['start_idx'])

def getInnerContents(tags_up, input):
  for t in tags_up:
    if t['tag_role'] == 'open_close' or t['tag_role'] == 'open_close_alt':
      continue
    else:
      t['innerHTML'] = input[t['end_idx']+1:t['closer']['start_idx']]
      t['outerHTML'] = input[t['start_idx']:t['closer']['end_idx']]
  return tags_up

def hasClosingTags(collected):
    result = False
    for no, c in enumerate(collected): 
        if c['tag_role'] == 'close' and no != 1:
            result = True
    return result


def identifyTags(input):
  collected_tags = []
  for tag in html_tags_stripped:
    as_open = re.findall(f'<{tag}(?=\s)', input)
    as_close = re.findall(f'</{tag}', input)
    ##handle openers
    current_idx = 0
    for o in as_open:
      meta_tag = {}
      meta_tag['tag_type'] = tag
      matcher = f"<{tag} />"
      meta_tag['start_idx'] = input.index(o, current_idx)
      meta_tag['end_idx'] = input.index('>', meta_tag['start_idx'])   
      meta_tag['with_attributes'] = input[meta_tag['start_idx']:meta_tag['end_idx'] +1]
      if isSelfCloser(matcher):
        meta_tag['tag_role'] = 'open_close'
        meta_tag['as_tag_identifier'] = matcher
      else:
        meta_tag['as_tag_identifier'] = f"<{tag}>"
        if meta_tag['end_idx'] > input.index('/', meta_tag['start_idx']):
          meta_tag['tag_role'] = 'open_close_alt'
        else:
          meta_tag['tag_role'] = 'open'
      specific = addSpecificAttributes(meta_tag)
      globals = addGlobalAttributes()
      meta_tag['allowed_attributes'] = mergeDict([globals, specific])  
      current_idx = meta_tag['end_idx']
      collected_tags.append(meta_tag)
    ##handle closers
    current_idx = 0
    for c in as_close:
      meta_tag = {}
      meta_tag['tag_type'] = tag
      meta_tag['tag_role'] = 'close'
      meta_tag['as_tag_identifier'] = f"{o}>"
      meta_tag['start_idx'] = input.index(c, current_idx)
      meta_tag['end_idx'] = input.index('>', meta_tag['start_idx'])
      meta_tag['with_attributes'] = ""
      collected_tags.append(meta_tag) 
      current_idx = meta_tag['end_idx'] +1
  return collected_tags


def parseStyleString(styles_, tag_styles):
  for val in styles_.split(";"):
    if (val == ""):
      continue
    else: 
      idx = val.index(":")
      kee = val[:idx].strip()
      value = val[idx+1:].strip()
      tag_styles[kee] = value
  return tag_styles

def parseAttributes(tags):
  for tag in tags: 
    #loop through the attribute keys
    for kee in tag['allowed_attributes'].keys():
      tag_with = tag['with_attributes']
      if f"{kee}=" not in tag_with:
        continue
        
      else:
        idx = tag_with.index(f"{kee}=")
        idx_equ = tag_with.index("=", idx)
        quot_type = tag_with[idx_equ + 1]
        idx_end = tag_with.index(quot_type, idx_equ + 2)
        if kee == 'style':
          tag['allowed_attributes'][kee] = parseStyleString(tag_with[idx_equ+2:idx_end], tag['allowed_attributes'][kee])
        else:
          tag['allowed_attributes'][kee] = tag_with[idx_equ+2:idx_end]
  return tags




def createSequence(sorted_tags):
  sequence = []
  for i, t in enumerate(sorted_tags):
    t['seq_id'] = f"{str(i)}-$$_{t['tag_type']}"
    sequence.append(t['seq_id'])
  return (sequence, sorted_tags)






def matchTags(tags_collected):
  tags = sortTags(tags_collected)
  updated_tags = []
  to_remove = []
  #sequence id = count-role_id_tagtype
  #count is unique in sequence for pair or self-closing
  #role_ids: 1 = open, 2 = close (needs to have same count), 3 = self-closing
  (seq, tags) = createSequence(tags)
  #fish out all self-closing tags

  for t in tags:
    if t['tag_role'] == 'open_close':
      s = t['seq_id']
      t['seq_id'] = s.replace('$$', "3")
      s_idx = seq.index(s)
      seq[s_idx] = t['seq_id']
      updated_tags.append(t)
      to_remove.append(t)
    if t['tag_role'] == 'open_close_alt':
      s = t['seq_id']
      t['seq_id'] = s.replace('$$', "3")
      s_idx = seq.index(s)
      seq[s_idx] = t['seq_id']
      updated_tags.append(t)
      to_remove.append(t)
  for item in to_remove:
    tags.remove(item)
  current_length = len(tags)
  # even though a while loop could work, it's lagging behind whith the remove statements and slips into an infinite loop
  for _ in range(0, current_length):
    current_length = len(tags)
    for i in reversed(range(0, current_length)):
      if i <= 1:
        break
      if tags[i]['tag_role'] == 'close' and tags[i-1]['tag_role'] == 'open':
        s = tags[i-1]['seq_id']
        s_close = tags[i]['seq_id']
        item_open = tags[i-1]
        item_open['seq_id'] = s.replace('$$', "1")
        seqIdAsDict = seqIdtoDict(item_open['seq_id'])
        item_close = tags[i]
        item_close['seq_id'] = f"{seqIdAsDict['seq_unique']}-2_{seqIdAsDict['seq_tag_type']}"
        seq[seq.index(s)] = item_open['seq_id']
        seq[seq.index(s_close)] = item_close['seq_id']
        item_open['closer'] = item_close
        updated_tags.append(item_open)
        tags.remove(item_open)
        tags.remove(item_close)
  # finish the last tags (what if the first tag is self-closing?)
  if len(tags) == 2:
    s = tags[0]['seq_id']
    s_close = tags[1]['seq_id']
    tags[0]['seq_id'] = s.replace('$$', "1")
    seq[seq.index(s)] = tags[0]['seq_id']    
    seqIdAsDict = seqIdtoDict(tags[0]['seq_id'])
    tags[1]['seq_id'] = f"{seqIdAsDict['seq_unique']}-2_{seqIdAsDict['seq_tag_type']}"
    seq[seq.index(s_close)] = tags[1]['seq_id']
    tags[0]['closer'] = tags[1]
    updated_tags.append(tags[0])
  return (seq, updated_tags)


# lifts style, id, class attributes to top level

def liftAttributes(tags):
  rel_attr = ['id', 'style', 'class']
  for tag in tags:
    for att in rel_attr:
      tag[att] = tag['allowed_attributes'][att]
      tag['allowed_attributes'].pop(att)
  return tags


def createChildrenReferences(seq, tags):
    for el in tags: 
        el["childrenRef"] = []
        el['children'] = []
        el['descendants'] = []
        el['text'] = ""
        el['isLastChild'] = False
    processed = []
    for no, s in enumerate(seq):
        in_process = []
        current = seqIdtoDict(s)
        for t in tags:
            look_for = ""
            if s == t['seq_id']:
                in_process.append(s)
                in_process.append(no)
                look_for = current['seq_unique']
                for i in range(no+1, len(seq)):
                    if seq[i].startswith(look_for):
                        in_process.append(i)
        processed.append(in_process)
    
    for p in processed:
        if len(p) <= 2:
            continue 
        for tag in tags: 
            if  tag['seq_id'] == p[0]:
                tag['childrenRef'] = seq[p[1]+1:p[2]]
                tag['isLastChild'] = isLastChild(tag['childrenRef'])
                if tag['isLastChild']:
                  tag['descendants'] = ""
                else:
                  tag['descendants'] = refToDescendants(tag, tags)
                tag['text'] = getText(tag)
                print('INNERHTML:',  tag['innerHTML'])
    
    return tags

def refToDescendants(tag, tags):
    children = []
    for ref in tag['childrenRef']:
        ref_split = seqIdtoDict(ref)
        id = ref_split['seq_tag_role']
        if id != "2":
            for t in tags:
                if t['seq_id'] == ref:
                    children.append(representElementAsString(t))
    kids = eliminateInDirects(children)
    return kids

def eliminateInDirects(ch):
  toRemove = []
  for c in ch:
    for h in ch:
      if h == c:
        continue
      if h in c:
        toRemove.append(h)
  for removee in toRemove:
    ch.remove(removee)
  
  return ch



def isLastChild(ref):
  return ref == []







  




def getText(tag):
  inner = tag['innerHTML']
  for child in tag['children']:
      inner = inner.replace(child, "")
  return inner







    

                            

                    
        



        





  






def mapHTMLString(input):
  tags = identifyTags(input)
  (seq, tags) = matchTags(tags)
  
  tags = getInnerContents(tags, input)
  tags = parseAttributes(tags)
  tags = liftAttributes(tags)
  createChildrenReferences(seq, tags)
  tags_asClass = []
  for e in tags:
    element = Element(e)
    tags_asClass.append(element)
  return (seq, tags_asClass)