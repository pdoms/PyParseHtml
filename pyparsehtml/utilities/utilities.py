def mergeDict(dictionaries):
  base = dictionaries[0]
  for d in range(1, len(dictionaries)):
    base.update(dictionaries[d])
  return base
  