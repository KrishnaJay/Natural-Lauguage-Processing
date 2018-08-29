import json
import time
import re

from collections import defaultdict
import sys
import random
start_time = time.time()

training_file_path = sys.argv[1]

fi = open(training_file_path, "r")

fh = open("vanillamodel.txt", "w")
fh1 = open("averagedmodel.txt", "w")
contents = fi.read()





word_true= dict()
weights1= dict()
weights2= dict()
word_line = defaultdict(list)
#word_line= dict()
bias1=0
a1=0
bias2=0
a2=0
counter=0
u1= dict()
u2= dict()
beta1= 0
beta2= 0
y_val= {'True': 1, 'Fake':-1, 'Pos':1, 'Neg':-1}
stop_words=['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was', 'were', 'will', 'with']



#print(len(contents.splitlines()))
line=contents.splitlines()
total=len(line)

for i in line:



   context1=i.split()[1]
   context2=i.split()[2]



   review= i.split()[3:]
   review_str = ' '.join(review)
   
   review_str = ((re.sub(r'[^\w\s]', ' ', review_str)).lower()).split()     #removing punctuation and conversion to lower case


   for j in review_str:
            if j not in stop_words:

               weights1[j]=0
               weights2[j]=0
               u1[j]=0
               u2[j]=0
               if (context1,context2,j,counter) in word_true:
                       word_true[(context1,context2,j,counter)]+=1

               else:
                       word_true[(context1,context2,j,counter)] = 1
                       word_line[counter].append((context1, context2, j,counter))

   counter = counter + 1



#print(word_true)

#print(word_line)


#print(word_count)

c=1

for k in range(30):

    
    for line in range(total):


            #print(line)
            a1=0
            a2 = 0
            tag1=[]
            tag2=[]
            for i in word_line[line]:

                a1=a1+ word_true[i]*weights1[i[2]]
                a2 = a2 + word_true[i] * weights2[i[2]]
                tag1=i[0]
                tag2=i[1]

            a1+=bias1
            a2 += bias2



            if a1*y_val[tag1]<=0:
                for j in word_line[line]:
                        weights1[j[2]]=weights1[j[2]]+ word_true[j]*y_val[tag1]
                        bias1=bias1+y_val[tag1]
                        u1[j[2]]=u1[j[2]]+y_val[tag1]*word_true[j]*c
                        beta1=beta1+ y_val[tag1]*c
            if a2 * y_val[tag2] <= 0:
                for j in word_line[line]:
                        weights2[j[2]] = weights2[j[2]] + word_true[j] * y_val[tag2]
                        bias2 = bias2 + y_val[tag2]
                        u2[j[2]] = u2[j[2]] + y_val[tag2] * word_true[j] * c
                        beta2 = beta2 + y_val[tag2] * c

    c=c+1




fh.write("\n Weights1 \n")
fh.write(repr(weights1))
fh.write("\n Weights2 \n")
fh.write(repr(weights2))
fh.write("\n Bias1 \n")
fh.write(repr(bias1))
fh.write("\n Bias2 \n")
fh.write(repr(bias2))

for i in weights1.keys():
    weights1[i]=weights1[i]-(1/c)*u1[i]
for i in weights2.keys():
    weights2[i]=weights2[i]-(1/c)*u2[i]
bias1= bias1- (1/c)*beta1
bias2= bias2- (1/c)*beta1

fh1.write("\n Weights1 \n")
fh1.write(repr(weights1))
fh1.write("\n Weights2 \n")
fh1.write(repr(weights2))
fh1.write("\n Bias1 \n")
fh1.write(repr(bias1))
fh1.write("\n Bias2 \n")
fh1.write(repr(bias2))


fh.close()
fi.close()

print("time elapsed: {:.2f}s".format(time.time() - start_time))

