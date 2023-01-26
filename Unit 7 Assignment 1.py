# Park University - CS152
# Unit 7 Assignment 1 - FA21
# Connor Tackkett 1690740

#def examAverages():
filename = input("Enter filename to read grades from: ")
fin = open(filename, "r")

nameSet = set()
examScores = [0,0,0,0]
numScores = 0
for line in fin:
  value = line.rstrip('\n').split(',')
  nameTuple = (value[0], value[1])
  if nameTuple in nameSet:
    print('WARNING: ' + value[0] + ' ' + value[1] + ' appears more than once in the input data')
  else:
    nameSet.add(nameTuple)
    ctr = 0
    for score in value[2:]:
      examScores[ctr] = examScores[ctr] + int(score)
      ctr += 1
    numScores += 1
  
for x in range(len(examScores)):
  print("average exam " + str(x + 1) + " score:  " + str(examScores[x] / numScores))

fin.close()

#if __name__ == "__main__":
#    main()