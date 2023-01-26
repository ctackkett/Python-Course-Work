# Park University - CS152
# Unit 7 Assignment 2 - FA21
# Connor Tackkett 1690740

import pathlib                                        # Used for checking if file exists

def ValidateValuesAreNumbers(valuesToCheck):          # This function takes in a set of values, strips the
  for valueToCheck in valuesToCheck:                  # leading or trailing white space, and checks whether
    valueToCheck = valueToCheck.strip()               # or not the values are number or not. This is done
    try:                                              # using a try and except, which sees if the value can be 
      int(valueToCheck)                               # converted into an integer or not.
    except:  
      return False
  return True

def CheckScoresInRange(valuesToCheck, lowestVal, highestVal):          # This function takes in a range of values, 
  for valueToCheck in valuesToCheck:                                   # and checks if the values within that range 
    intValue = int(valueToCheck)                                       # fall into another range of values given in 
    if intValue < lowestVal or intValue > highestVal:                  # lowestVal and highestVal parameters. 
      return False
  return True

def FinalGrade(classFinal):                                            # This function calculates the letter grade based on the percentage
  letterGrade = ''                                                     # that the student earned total, which is the classFinal variable.
  if classFinal <= 100 and classFinal >= 90:
    letterGrade = 'A'
  elif classFinal < 90 and classFinal >= 80:
    letterGrade = 'B'
  elif classFinal < 80 and classFinal >= 70:
    letterGrade = 'C'
  elif classFinal < 70 and classFinal >= 60:
    letterGrade = 'D'
  else:
    letterGrade = 'F'
  return letterGrade

def ConvertValuesToInt(valuesToScore):                                 # This function converts the lsit values to integers, so it can be 
  for i in range(0, len(valuesToScore)):                               # checked to see if the grades are numbers or not
    valuesToScore[i] = int(valuesToScore[i])
  return valuesToScore

def CalculateGrade(valuesToCheck, pointsPossiblePerValue, dropLowest): # This function calculates the grade, as a percentage, based on the
  valuesToCheck = ConvertValuesToInt(valuesToCheck)                    # possible points per grade per catagory. Also it deals with dropping
  numOfValues = len(valuesToCheck)                                     # the lowest exam score.
  totalEarned = 0
  for valueToCheck in valuesToCheck:
    totalEarned += valueToCheck
  
  if dropLowest == True:                                               # If the grade type is exam, the lowest score is dropped.
    numOfValues -= 1
    totalEarned = totalEarned - min(valuesToCheck)

  totalAvailable = numOfValues * pointsPossiblePerValue

  return (totalEarned / totalAvailable) * 100
                                  
def main():
  
  inputFilename = 'grades.csv'                                            # Initializing input and output file names
  outputFilename = 'final_grades.csv'                                                  

  path = pathlib.Path('final_grades.csv')                                 # nothing is over-written if the file already exists
  if (path.exists()) == True:
    print('ERROR: ' + outputFilename + ' file already exists.')
  else:
    try:   # for opening input file          
      inputFile = open(inputFilename, "r")                                  

      try: # for opening output file   
        outputFile = open(outputFilename, "a")

        lineCtr = 0
        for line in inputFile:
          lineCtr += 1                            
          # validate each line of the filename
          lineValues = line.split(',')
          if len(lineValues) < 24:                                                          # This series of if statements 
            print('Line ' + str(lineCtr) + ' does not have enough values')                  # makes sure there are 24 values per
          elif len(lineValues) > 24:                                                        # line. If there are, the rest of the
            print('Line ' + str(lineCtr) + ' has too many values')                          # code is run.
          elif lineValues[0].strip().isdigit() or lineValues[1].strip().isdigit():          # If the student names are not
            print('Line ' + str(lineCtr) + ' has an invalid student name')                    # strings, throw an error, otherwise
          else:                                                                             # continue.
      #      if ValidateValuesAreNumbers(lineValues[2:10]) == False:
      #        print('Line ' + str(lineCtr) + ' has bad values in the lab scores')
            if ValidateValuesAreNumbers(lineValues[2:10]) == False:                         # values 2-24 are validated with
              print('Line ' + str(lineCtr) + ' has invalid values in the assignment scores')# their coresponding expected values
            elif CheckScoresInRange(lineValues[2:10], 0, 10) == False:                      # First it is checked if the values
              print('Line ' + str(lineCtr) + ' has assignment scores that are out of range')# are numbers. Then it is checked if 
            elif ValidateValuesAreNumbers(lineValues[10:18]) == False:                      # the values are in the given range.
              print('Line ' + str(lineCtr) + ' has invalid values in the lab scores')
            elif CheckScoresInRange(lineValues[10:18], 0, 30) == False:
              print('Line ' + str(lineCtr) + ' has lab scores that are out of range')
            elif ValidateValuesAreNumbers(lineValues[18:20]) == False:
              print('Line ' + str(lineCtr) + ' has invalid values in the project scores')
            elif CheckScoresInRange(lineValues[18:20], 0, 100) == False:
              print('Line ' + str(lineCtr) + ' has project scores that are out of range')
            elif ValidateValuesAreNumbers(lineValues[18:20]) == False:
              print('Line ' + str(lineCtr) + ' has invalid values in the exam scores')
            elif CheckScoresInRange(lineValues[20:], 0, 160) == False:
              print('Line ' + str(lineCtr) + ' has exam scores that are out of range')
            else:         
              # If the values all validate correctly 
              prepScore = CalculateGrade(lineValues[2:10], 10, False)                                 # Function call calculates percentage 
              labScore = CalculateGrade(lineValues[10:18], 30, False)                                 # grade for each grade catagory.
              projectScore = CalculateGrade(lineValues[18:20], 100, False)
              examScore = CalculateGrade(lineValues[20:], 160, True)
              classFinal = (prepScore*.24 + labScore*.08 + projectScore*.20 + examScore*.48)
              outputFile.write(lineValues[0].strip() + ',' + lineValues[1].strip() + ',')
              outputFile.write(str(round(prepScore, 1)) + ',')                                        # New data is written to file
              outputFile.write(str(round(labScore, 1)) + ',')
              outputFile.write(str(round(projectScore, 1)) + ',') 
              outputFile.write(str(round(examScore, 1)) + ',')
              outputFile.write(str(round(prepScore*.08 + labScore*.24 + projectScore*.20 + examScore*.48, 1)) + ',')
              letterGrade = FinalGrade(classFinal)
              outputFile.write(letterGrade + '\n')
        outputFile.close()
        inputFile.close()
      except:                                                                           # Errors are thrown if the file cannot be created 
        print('ERROR: unable to create output file')                                    # or if the file is not found
    except:
      print('ERROR: grades.csv file not found')     

if __name__ == "__main__":
  main()