
import operator
import ast
import math
import time
import sys
import sys
import re
import math
start_time = time.time()
training_file_path1 = sys.argv[1]
training_file_path2 = sys.argv[2]

fh = open(training_file_path1, "r")
f = open(training_file_path2, "r")

fo = open("percepoutput.txt", "w")

contents = f.read()

learnt_data = fh.read()
#print(learnt_data)
stop_words=['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with']
weight1=ast.literal_eval(learnt_data.splitlines()[2])
#print(weight1)
weight2=ast.literal_eval(learnt_data.splitlines()[4])
bias1=ast.literal_eval(learnt_data.splitlines()[6])
bias2=ast.literal_eval(learnt_data.splitlines()[8])


line=contents.splitlines()

total=len(line)

for i in line:


  id=i.split()[0]




  review= i.split()[1:]

  review_str = ' '.join(review)
  #print(review_str)
  
  review_str = ((re.sub(r'[^\w\s]', ' ', review_str)).lower()).split()   #removing punctuation and conversion to lower case
  #print(review_str)
  a1 = 0
  a2 = 0
  word_true = dict()
  #print(review_str)
  for i in review_str:


      if i not in stop_words:
          if i in word_true:
              word_true[i] += 1
          else:
              word_true[i] = 1
  #print(word_true)
  for j in word_true.keys():
    if j in weight1.keys():
            a1 = a1+ weight1[j]*word_true[j]
    if j in weight2.keys():
            a2 = a2+ weight2[j]*word_true[j]
  #print(a1+bias1)
  if a1+bias1>0:
      temp1="True"
  else:
      temp1 = "Fake"
  if a2+bias2 > 0:
      temp2 = "Pos"
  else:
      temp2 = "Neg"

  fo.write(id + " " + temp1 + " " + temp2 + "\n")





fo.close()
fh.close()

print ("time elapsed: {:.2f}s".format(time.time() - start_time))

