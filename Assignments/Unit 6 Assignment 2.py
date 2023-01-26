# Park University - CS152
# Unit 6 Assignment 2 - FA21
# Connor Tackkett 1690740

def main():
  
    scores_total = 0
    num_scores = 0

    filename = input("Enter filename to read grades from: ")

    fin = open(filename, "r")

    for line in fin:
      values = line.split(",")
      scores_total += int(values[1])
      num_scores += 1

    print(scores_total / num_scores)

    if __name__ == '__main__':
      main()
  