import json
import time
import re
from collections import defaultdict
import sys
start_time = time.time()
training_file_path = sys.argv[1]
fi = open(training_file_path, "r")

fh = open("nbmodel.txt", "w")
contents = fi.read()




word_count=dict()
word_true= dict()
word_pos= dict()
word_fake= dict()
word_neg= dict()
true_count= 0
fake_count= 0
pos_count= 0
neg_count= 0
t=0
f=0
n=0
p=0


stop_words=['a', 'able', 'about', 'above', 'across', 'again', "ain't", 'all', 'almost', 'along', 'also', 'am',
              'among',
              'amongst', 'an', 'and', 'anyhow', 'anyone', 'anyway', 'anyways', 'appear', 'are', 'around', 'as', "a's",
              'aside', 'ask', 'asking', 'at', 'away', 'be', 'became', 'because', 'become', 'becomes', 'becoming',
              'been',
              'before', 'behind', 'below', 'beside', 'besides',
              'between', 'beyond', 'both', 'brief', 'but', 'by', 'came', 'can', 'come', 'comes', 'consider',
              'considering', 'corresponding', 'could', 'do', 'does', 'doing', 'done', 'down', 'downwards'
    , 'during', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'etc', 'even', 'ever', 'every', 'ex',
              'few', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'from', 'further', 'furthermore',
              'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'happens',
              'has', 'have', 'having', 'he', 'hed', 'hence', 'her'
    , 'here', 'hereafter', 'hereby', 'herein', "here's", 'hereupon', 'hers', 'herself', "he's", 'hi', 'him', 'himself',
              'his', 'how', 'hows', 'i', "i'd", 'ie', 'if', "i'll", "i'm", 'in', 'inc', 'indeed', 'into', 'inward',
              'is',
              'it', "it'd", "it'll", 'its', "it's", 'itself', "i've", 'keep', 'keeps', 'kept', 'know', 'known', 'knows',
              'lately', 'later', 'latter', 'latterly',
              'lest', 'let', "let's", 'looking', 'looks', 'ltd', 'may', 'maybe', 'me', 'mean', 'meanwhile', 'might',
              'most', 'my', 'myself', 'name', 'namely', 'nd', 'near', 'nearly', 'need', 'needs',
              'neither', 'next', 'nine', 'no', 'non', 'now', 'nowhere', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old',
              'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'ought',
              'our', 'ours', 'ourselves', 'out', 'over', 'own', 'per', 'placed', 'que', 'quite', 're', 'regarding',
              'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed',
              'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'seven', 'several', 'she', "she'd",
              "she'll", "she's", 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something',
              'sometime',
              'sometimes', 'somewhat', 'somewhere', 'soon', 'specified', 'specify', 'specifying', 'still', 'sub',
              'such',
              'sup', 'sure', 'take', 'taken', 'tell', 'tends', 'th', 'than', 'that', 'thats', "that's", 'the', 'their',
              'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore',
              'therein',
              'theres', "there's", 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'think',
              'third', 'this', 'those', 'though', 'three', 'through', 'thru', 'thus', 'to', 'together'
    , 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', "t's", 'twice', 'two', 'un',
              'under', 'up', 'upon', 'us', 'use', 'used', 'uses', 'using', 'usually', 'value', 'various', 'very', 'via',
              'viz', 'vs', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll", 'went', 'were', "we're",
              "weren't", "we've", 'what', 'whatever', "what's", 'when', 'whence', 'whenever', "when's", 'where',
              'whereafter', 'whereas', 'whereby', 'wherein', "where's", 'whereupon', 'wherever', 'whether', 'which',
              'while', 'whither', 'who', 'whoever'
    , 'whole', 'whom', "who's", 'whose', 'why', "why's", 'will', 'willing', 'wish', 'with', 'within', 'without',
              "won't", 'would', "wouldn't", 'yes', 'yet', 'you', "you'd", "you'll", 'your',
              "you're", 'yours', 'yourself', 'yourselves', "you've"]



#print(len(contents.splitlines()))
line=contents.splitlines()
total=len(line)

for i in line:


   context1=i.split()[1]
   context2=i.split()[2]


   if context1=="True":
       t+=1
   else:
       f+=1
   if context2=="Pos":
       p+=1
   else:
       n+=1

   review= i.split()[3:]
   review_str = ' '.join(review)
   review_str = ((re.sub(r'[^\w\s]', '', review_str)).lower()).split()     #removing punctuation and conversion to lower case

   #print(review_str)
   for j in review_str:
            if j not in stop_words:
               if j in word_count:
                       word_count[j] += 1
               else:
                       word_count[j] = 1
               if context1 == "True":
                   true_count+=1
                   if ('True',j) in word_true:
                       word_true[('True',j)]+=1
                   else:
                       word_true[('True', j)] = 1

               if context1 == "Fake":
                   fake_count+=1
                   if ('Fake',j) in word_fake :
                       word_fake[('Fake',j)]+=1
                   else:
                       word_fake[('Fake', j)] = 1
               if  context2== "Pos":
                   pos_count+=1
                   if ('Pos',j) in word_pos :
                       word_pos[('Pos',j)]+=1
                   else:
                       word_pos[('Pos', j)] = 1
               if context2 == "Neg":
                   neg_count+=1
                   if ('Neg',j) in word_neg :
                       word_neg[('Neg',j)]+=1
                   else:
                       word_neg[('Neg', j)] = 1


vocab_size= len(word_count)


for i in word_count.keys():
        if ('True',i) in word_true.keys():
            word_true[('True',i)]= (float(word_true[('True',i)]+1)/(true_count+vocab_size))
        else:
            word_true[('True',i)]= (float(1/(true_count+vocab_size)))
        if ('Fake',i) in word_fake.keys():
            word_fake[('Fake',i)]= (float(word_fake[('Fake',i)]+1)/(fake_count+vocab_size))
        else:
            word_fake[('Fake',i)]= (float(1/(fake_count+vocab_size)))
        if ('Pos',i) in word_pos.keys():
            word_pos[('Pos',i)]= (float(word_pos[('Pos',i)]+1)/(pos_count+vocab_size))
        else:
            word_pos[('Pos',i)]= (float(1/(pos_count+vocab_size)))
        if ('Neg',i) in word_neg.keys():
            word_neg[('Neg',i)]= (float(word_neg[('Neg',i)]+1)/(neg_count+vocab_size))
        else:
            word_neg[('Neg',i)]=float(1/(neg_count+vocab_size))

#print(t)
#print(f)



t=(float(t/total))
f=(float(f/total))
p=(float(p/total))
n=(float(n/total))






fh.write("True prob \n")
fh.write(repr(word_true))
fh.write("\n Fake prob \n")
fh.write(repr(word_fake))
fh.write("\n Pos prob \n")
fh.write(repr(word_pos))
fh.write("\n Neg prob \n")
fh.write(repr(word_neg))
fh.write("\nprior true\n")
fh.write(repr(t))
fh.write("\nprior fake\n")
fh.write(repr(f))
fh.write("\nprior pos\n")
fh.write(repr(p))
fh.write("\nprior neg\n")
fh.write(repr(n))
fh.write("\n Vocab size \n")
fh.write(repr(vocab_size))
fh.write("\n True count \n")
fh.write(repr(true_count))
fh.write("\n Fake count \n")
fh.write(repr(fake_count))
fh.write("\n Pos count \n")
fh.write(repr(pos_count))
fh.write("\n Neg count\n")
fh.write(repr(neg_count))
fh.close()
fi.close()

print("time elapsed: {:.2f}s".format(time.time() - start_time))

