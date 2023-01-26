height = (int(input("Please enter a height: ")))
width = (int(input("Please enter a width: ")))
row = 1                             #declare and initialize row loop counter
while row <= height:
  if row == 1 or row == height:     #deals with the problem of top and bottom cap
    print("*" * width)
  else:                             #prints middle rows
    print("*" + (" " * (width - 2) + "*"))
  row += 1                          #incrementation of the row loop counter

