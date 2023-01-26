height = (int(input("Please enter a height: ")))
width = (int(input("Please enter a width: ")))
print("*" * width)
for x in range(height):
    print("*" + (" " * (width - 2) + "*"))
print("*" * width)
