
import operator
import ast
import math
import time
import sys
import sys
import re
import math
start_time = time.time()
training_file_path = sys.argv[1]
f = open(training_file_path, "r")
fh = open("nbmodel.txt", "r")
fo = open("nboutput.txt", "w")

contents = f.read()

learnt_data = fh.read()
#print(learnt_data)
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
word_true=ast.literal_eval(learnt_data.splitlines()[1])
word_fake=ast.literal_eval(learnt_data.splitlines()[3])
word_pos=ast.literal_eval(learnt_data.splitlines()[5])
word_neg=ast.literal_eval(learnt_data.splitlines()[7])
prior_true= ast.literal_eval(learnt_data.splitlines()[9])
prior_fake= ast.literal_eval(learnt_data.splitlines()[11])
prior_pos= ast.literal_eval(learnt_data.splitlines()[13])
prior_neg= ast.literal_eval(learnt_data.splitlines()[15])
vocab= ast.literal_eval(learnt_data.splitlines()[17])
#print(ast.literal_eval(learnt_data.splitlines()[15]))
line=contents.splitlines()

total=len(line)

for i in line:


  id=i.split()[0]




  review= i.split()[1:]

  review_str = ' '.join(review)
  #print(review_str)
  review_str = ((re.sub(r'[^\w\s]', '', review_str)).lower()).split()   #removing punctuation and conversion to lower case
  #print(review_str)

  p_true = 1
  p_fake = 1
  p_pos = 1
  p_neg = 1
  for i in review_str:
      if i not in stop_words:

          if ('True',i) in word_true.keys():
            p_true  +=math.log(word_true[('True',i)])

           #print(p_true,('True',i) )
          if ('Fake',i) in word_fake.keys():
           p_fake+= math.log(word_fake[('Fake',i)])
          if ('Pos',i) in word_pos.keys():
           p_pos+= math.log(word_pos[('Pos',i)])
          if ('Neg',i) in word_neg.keys():
           p_neg+= math.log(word_neg[('Neg',i)])

  #print(review_str)
  #print(p_true)


  p_true += math.log(prior_true)
  p_fake += math.log(prior_fake)
  p_pos += math.log(prior_pos)
  p_neg += math.log(prior_neg)


  if(p_true>p_fake):
      temp1="True"
  else:
      temp1="Fake"
  if(p_pos>p_neg):
      temp2= "Pos"
  else:
      temp2= "Neg"

  fo.write(id+" "+temp1+" "+temp2+"\n")


fo.close()
fh.close()

print ("time elapsed: {:.2f}s".format(time.time() - start_time))

