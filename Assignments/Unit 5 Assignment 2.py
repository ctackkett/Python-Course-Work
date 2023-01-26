def list_shift_forward(ls):
  newls = []
  
  newls.insert(0, ls[-1])
  
  for x in range(1, len(ls)):
    newls.insert(x, ls[x-1])
    
  
  return newls


# one line solution 
def list_shift_forward(ls):
  return ls[-1:] + ls[:-1]