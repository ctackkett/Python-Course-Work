# Connor Tackkett
# Function finds average of top three scores.
def exam_average(exam1, exam2, final_mc, final_practical):
  minval=min(exam1, exam2, final_mc, final_practical)
  total= exam1 + exam2 + final_mc + final_practical - minval
  return int(round(total / 3.0))

print(exam_average(54, 82, 64, 73))
print(exam_average(74, 98, 87, 99))
print(exam_average(100, 0, 0, 0))
print(exam_average(0, 0, 100, 100))
print(exam_average(0, 100, 0, 0))
print(exam_average(100, 100, 100, 100))
print(exam_average(12, 13, 14, 15))
print(exam_average(0, 100, 50, 50))
print(exam_average(100, 90, 92, 73))
print(exam_average(90, 100, 98, 90))
print(exam_average(100, 100, 90, 100))
print(exam_average(21, 62, 84, 90))
print(exam_average(100, 32, 74, 80))