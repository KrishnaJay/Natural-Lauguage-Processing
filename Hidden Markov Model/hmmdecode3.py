import operator
import ast
import math
import time
import sys
import sys
start_time = time.time()
training_file_path = sys.argv[1]
f = open(training_file_path, "r", encoding='utf-8-sig')
fh = open("hmmmodel.txt", "r", encoding='utf-8-sig')
fo = open("hmmoutput.txt", "w", encoding='utf-8-sig')

contents = f.read()

learnt_data = fh.read()

transition_prob = {}
tag_set = {}
emission_word={}
emission_prob = {}



tag_set = ast.literal_eval(learnt_data.splitlines()[1])
prev_tag= ast.literal_eval(learnt_data.splitlines()[3])
transition_prob = ast.literal_eval(learnt_data.splitlines()[5])
emission_prob = ast.literal_eval(learnt_data.splitlines()[7])
emission_word= ast.literal_eval(learnt_data.splitlines()[9])
tags=ast.literal_eval(learnt_data.splitlines()[11])
del tag_set['start']

length = len(tag_set)
l=len(tags)
i = 0
for key in tag_set:
    tag_set[key] = i
    i += 1



for i in contents.splitlines():

    prob_matrix = {}
    temp_storage = i.split()
    # change the order of for loops, first cut down states by selecting only emision


    word=temp_storage[0]
    if word not in emission_word:  # unknown word
        for state in tags:
            if ("start", state) in transition_prob:
                prob_matrix[(word, state, 0)] = (transition_prob[('start', state)], 'start')
            else:
                if "start" in prev_tag:
                    prob = prev_tag["start"]
                else:
                    prob=0
                    tp = 1 / (prob + l)
                    prob_matrix[(word, state,0)] = (tp, 'start')
    #print(word,type(word))
    else:
        states = emission_word[word]
        for state in states:
            if ("start", state) in transition_prob:
                probability = abs(transition_prob[("start", state)] * emission_prob[(word, state)])
                prob_matrix[(word, state, 0)] = (probability, "start")
            else:
                if "start" in prev_tag:
                    prob = prev_tag["start"]
                else:
                    prob=0
                tp = 1 / (prob + l)
                probability = abs(tp * emission_prob[(word, state)])
                prob_matrix[(word, state, 0)] = (probability, "start")

    num_of_words = len(temp_storage)
        #print(temp_storage[num_of_words-1])
        #word = 0
    #print("check-1")
    for word in range(1, num_of_words):
        #print("check-2")
        if temp_storage[word] not in emission_word: #dict word -> set(states) -> emission prob > 0\\\
            #print("check-3")
            max_transition = float(-1)
            bp = None
            for state in tags:
                for s in tags:
                    if (temp_storage[word-1], s, word - 1) in prob_matrix:
                        if (s, state) in transition_prob:
                            p = abs(prob_matrix[(temp_storage[word-1], s, word - 1)][0] * transition_prob[(s, state)])
                            #print(p)
                            if max_transition < p:
                                max_transition = p
                                #print(p)
                                bp = s
                        else:  # smoothing
                            if s in prev_tag:

                                prob = prev_tag[s]
                            else:
                                prob=0
                            tp = 1 / (prob + l)
                            p = abs(prob_matrix[(temp_storage[word-1], s, word - 1)][0] * tp)
                            if max_transition < p:
                                max_transition = p
                                bp = s
                                #print(bp)
                prob_matrix[(temp_storage[word], state, word)] = (max_transition, bp)


        else:
            #print("check-4")
            states = emission_word[temp_storage[word]]
            max_transition = float(-1)
            bp = None
            for state in states:
                #print("check-5")
                for s in tags:
                    #print("check-6")
                    if (temp_storage[word-1], s, word - 1) in prob_matrix:
                        #print("check-7")
                        if (s, state) in transition_prob:

                            p = abs(prob_matrix[(temp_storage[word-1], s, word - 1)][0] * transition_prob[(s, state)])
                            if max_transition < p:
                                max_transition = p
                                bp = s
                        else:  # smoothing
                            if s in prev_tag:
                                prob = prev_tag[s]
                            else:
                                prob=0
                            tp = 1 / (prob + l)
                            p = abs(prob_matrix[(temp_storage[word-1], s, word - 1)][0] * tp)
                            if max_transition < p:
                                max_transition = p
                                bp = s
                    #print(s)
                #print(bp)
                probability = max_transition * emission_prob[(temp_storage[word], state)]
                prob_matrix[(temp_storage[word], state, word)] = (probability, bp)



    #print(prob_matrix)

    tag_list = []
    last = None
    max = -1
    for state in tags:
        #print(state,"st")
        if (temp_storage[num_of_words - 1], state, num_of_words - 1) in prob_matrix:
            if max < prob_matrix[(temp_storage[num_of_words - 1], state, num_of_words - 1)][0]:
                max = prob_matrix[(temp_storage[num_of_words - 1], state, num_of_words - 1)][0]
                last = state
    if isinstance(last, str):
        #print("feg")
        tag_list.append(last)
    #print(last,"dfdsF")
    i = num_of_words - 2

    while i >= 0:
        #print(last)
        if isinstance(last, str):
            p_val = prob_matrix[(temp_storage[i + 1], last, i + 1)]

            last = p_val[1]
            #print(last,"fgf")
            tag_list.append(p_val[1])
        i -= 1
    #print(tags)
    tag_list = list(reversed(tag_list))

    final = ""
    i = 0
    #print(len(temp_storage))
    #print(len(tags))
    while i < num_of_words:
        final += temp_storage[i] + "/" + tag_list[i]
        if i != num_of_words - 1:
            final += " "
        i += 1
   # print(final)




        #print(i.split()[x] + "/" + tag_list[len(tag_list)-1  - x])
    fo.write(final)
    fo.write("\n")

fo.close()
fh.close()

print ("time elapsed: {:.2f}s".format(time.time() - start_time))