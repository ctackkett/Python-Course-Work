def remove_tags(txt):
  acc = ""
  intag = False
  for x in txt:
    if x == '<':
      intag = True
    elif x == '>':
      intag = False
    elif not intag:
      acc = acc + x    

  return acc
print(remove_tags('one <b>tag</b> here'))


