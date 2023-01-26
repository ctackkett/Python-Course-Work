# Connor Tackkett 
# Function will find average of list of scores after dropping lowest score, to one decimal place.
def raw_postlab_score(scores):
  minval=min(scores)
  total = 0.0
  for x in scores: #had to loop through list to add values.
    total = total + x
  total = total - minval
  return total / (len(scores) - 1) #had to subtract one off length of scores.

print(raw_postlab_score([4.5, 6]))
