def greatest_common_divisor(a,b):
  r = 0
  temp = a 
  a = b
  b = temp
  
  while True:
    r = a % b
    if r == 0:
      break
    a = b
    b = r
    
  return b

print(greatest_common_divisor(10,10))