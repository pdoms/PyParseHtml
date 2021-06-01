import re
import copy

from .element import Element
from .utils import isSelfCloser, mergeDict, representElementAsString, seqIdtoDict, getTagBySeqId
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
      meta_tag['rest_string'] = input[meta_tag['end_idx'] + 1:]  
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
      meta_tag['rest_string'] = input[meta_tag['end_idx'] + 1:]  
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



def matchTokens(tags_collected):
  tags = sortTags(tags_collected)
  (seq, tags) = createSequence(tags)
  updated_tags = [] 
  to_remove = []
  no_of_open = 0
  for t in tags:
    if t['tag_role'] == 'open':
      no_of_open += 1
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
  #count open tags?
  current_length = len(tags)
  while no_of_open > 0:
    for i in reversed(range(0, current_length)):
      open = {}
      close = {}
      if tags[i]['tag_role'] == 'open':
        open = tags[i]
        open_s = tags[i]['seq_id']
        open['seq_id'] = open['seq_id'].replace('$$', "1")
        seq[seq.index(open_s)] = open['seq_id']
        open_seq = seqIdtoDict(open['seq_id'])
        for f in range(i, len(tags)):
          if tags[f]['tag_role'] == 'close':
            close = tags[f]
            close_s = tags[f]['seq_id']
            close['seq_id'] = f"{open_seq['seq_unique']}-2_{open_seq['seq_tag_type']}"
            seq[seq.index(close_s)] = close['seq_id']
            break
        # wrong - needs to be a copy of the unfinished seq ID
        open['closer'] = close
        updated_tags.append(open)
        tags.remove(open)
        tags.remove(close)
        break
    current_length = len(tags)
    no_of_open -= 1
  return (seq, updated_tags)   

# lifts style, id, class attributes to top level

def liftAttributes(tags):
  rel_attr = ['id', 'style', 'class']
  for tag in tags:
    for att in rel_attr:
      tag[att] = tag['allowed_attributes'][att]
      tag['allowed_attributes'].pop(att)
  return tags

def getText(seq_id, next_tag, tags):
  
  element = getTagBySeqId(tags, seq_id['seq_id'])

  text_after = element['rest_string']
  idx = -1
  next = next_tag['seq_tag_type']
  if next_tag['seq_tag_role'] == '2':
    idx = text_after.find(f'</{next}')
  else:
    idx = text_after.find(f'<{next}')
  if idx == -1:
    return ''
  else:
    return '$_text_$_' + text_after[0:idx]
  


def handleTexts(sqs, tgs):
  items = []
  for s in range(0, len(sqs) - 1):
    item = {}
    seq_current = seqIdtoDict(sqs[s])
    seq_next = seqIdtoDict(sqs[s+1])
    item['after'] = sqs[s]
    item['text'] = getText(seq_current, seq_next, tgs)
    items.append(item)
  for i in items:
    if i['text'] != '$_text_$':
      idx = sqs.index(i['after'])
      sqs.insert(idx+1, i['text'])
  return sqs


#find a way to represent dom as dictionary with levels of nesting (irrelevant of text, just to have it ready)
#e.g: 
#body: {
#   div: {
#     text: ...
#     p: {},
#     p: {},
#     p: {
#       img: {}
#       } 
#     }
#   div: {}
# }
#
#
#
#

    
def mapHTMLString(input):
  tags = identifyTags(input)
  (seq, tags) = matchTokens(tags)
  tags = getInnerContents(tags, input)
  tags = parseAttributes(tags)
  tags = liftAttributes(tags)
  seq = handleTexts(seq, tags)
  tags_asClass = []
  for e in tags:
    element = Element(e)
    tags_asClass.append(element)
  return (seq, tags_asClass)