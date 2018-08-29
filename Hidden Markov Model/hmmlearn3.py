import json
import time
from collections import defaultdict
import sys
start_time = time.time()
training_file_path = sys.argv[1]
f = open(training_file_path, "r", encoding='utf-8-sig')

fh = open("hmmmodel.txt", "w", encoding='utf-8-sig')
contents = f.read()

def toJson(dict):
   result  =  json.dumps(dict)

   return  result




unknown_state_transition={}
#emission_words={}
transition=dict()
emission = dict()
tag_count=dict()
tag_count['start']=0
word_count=dict()
prev_tag={}
prev_tag['start']=0
tags= set()
#print(len(contents.splitlines()))
for i in contents.splitlines():

   wordsplit= i.split(" ")

   slashsplit= wordsplit[0].rsplit("/",1)
   if ('start', slashsplit[1]) in transition:
       transition[('start',slashsplit[1])] += 1
   else:
       transition[('start', slashsplit[1])] = 1

   prev_tag['start']+=1

   length = len(i.split())
   for word in range(0, length):

       partition = i.split()[word].rsplit('/', 1)
       if partition[1] in tag_count:
           tag_count[partition[1]]+=1
       else:
           tag_count[partition[1]] = 1

       if partition[1] not in tags:
            tags.add(partition[1])
       if word == (length - 1):
           next_tag='end'
       else:

           next_partition = i.split()[word + 1].rsplit("/",1)

           next_tag= next_partition[1]
           if partition[1] in prev_tag:
               prev_tag[partition[1]] += 1
           else:
               prev_tag[partition[1]]=1

       if (partition[1],next_tag) in transition:
           transition[(partition[1], next_tag)]+=1
       else:
           transition[(partition[1], next_tag)] = 1
           #known_state_transition=




       if (partition[0], partition[1]) in emission:
           emission[(partition[0], partition[1])] += 1
       else:
           emission[(partition[0], partition[1])] = 1
#print(tags)
tag_state_number= len(tags)
#print(tag_count)
#print(tag_count)
#print(transition)
#print(prev_tag)



for key in transition.keys():
       if "end" == key[1]:
           continue
       transition[key] = (transition[key]+1) / (float(prev_tag[key[0]]) +tag_state_number)

#for key in tag_count.keys()


emission_words = dict()
transitions_words= defaultdict(list)



for key in emission.keys():
    if key[0] in emission_words:
        emission_words[key[0]].add(key[1])
    else:
        emission_words[key[0]] = set()
        emission_words[key[0]].add(key[1])
    emission[key] /= float(tag_count[key[1]])

#print(emission_words)
for key, value in emission_words.items():
    emission_words[key] = list(emission_words[key])
#print(prev_tag)
fh.write("Tag Set \n")
#fh.write(str(prev_tag['start']))
fh.write(repr(tag_count))
fh.write("\nPrev tag \n")
fh.write(repr(prev_tag))
fh.write("\nTransition Probabilities \n")
fh.write(repr(transition))
fh.write("\n Emission Probabilities \n")
#print(emission)
fh.write(repr(emission))
fh.write("\n Emission words \n")
fh.write(repr(emission_words))
fh.write("\n Tags\n")
fh.write(repr(tags))

fh.close()
f.close()
print ("time elapsed: {:.2f}s".format(time.time() - start_time))

