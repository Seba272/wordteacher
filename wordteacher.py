#!/usr/bin/python3
import time
import random
import json
from os import path

this_file = "word_teacher_v1.0"
log_file = "wt.log"
log_separator = " ; "
diz_file="Suomi-English.csv"
diz_data_file = diz_file + ".wt"
diz_data=[] 
strat_exercise = [2,2,2,2,2]

def write_log(qst,ans_c,ans):
    with open(log_file,"a") as fl:
        fl.write(format(time.time().__int__(),"x"))
        fl.write(log_separator)
        fl.write(this_file)
        fl.write(log_separator)
        fl.write(qst)
        fl.write(log_separator)
        fl.write(ans_c)
        fl.write(log_separator)
        fl.write(ans)
        fl.write(" \n")

# [[0:lang0, 1:lang1, 2:number of positive tests, 3:number of negative tests, 4:date of inizialization, 5:date of last test],...]
def diz_upload(f=diz_file):
    dd = []
    today = int(time.time())
    with open(f,"r") as fd:
        for line in fd:
            if line[0]=="%":
                continue
            if line[0]=="!":
                line = line[1:]
            a = line.split(";")
            a = [b.strip() for b in a]
            a.append(0) # 2: positive tests
            a.append(0) # 3: negative tests
            a.append(today) # 4: date of inizialization
            a.append(0) # 5: date of last test
            dd.append(a)
    return dd

def diz_data_save(f=diz_data_file,dd=diz_data):
    with open(f,"w") as fl:
        json.dump(dd,fl)

def diz_data_upload(f=diz_data_file,dd=diz_data):
    if path.exists(diz_data_file):
        with open(diz_data_file, "r") as fup:
            dd = json.load(fup)
    else:
        dd = diz_upload()
    return dd

# [[index in diz,level],...]
def choose_batch(dd=diz_data,n_words=5):
    a = []
    today = int(time.time())
    strat_repetitions = max(strat_exercise)
    strat_days = len(strat_exercise)
#    print("choose_batch: diz_data, dd: \n",dd)
#    print("choose_batch: today \n",today)
    for w in range(1,len(dd)) :
        word_days = max(int((dd[w][5]-today)/86400),0)
        word_level = dd[w][2]-dd[w][3]
#        print("choose_batch: w=",w,"; word_days=",word_days,"; word_level=",word_level,"; strat_days=",strat_days,"; sum=",sum([strat_exercise[j] for j in range(word_days)]),"; k=",k,"\n")
        if word_days < strat_days and word_level < sum([strat_exercise[j] for j in range(word_days+1)]) :
            a.append([w,strat_exercise[word_days]])
        if len(a) >= n_words :
            break
#    print("choose_batch: a:\n",a)
    return a

def testing(test_batch):
    number_words = len(test_batch)
    while number_words > 0 :
        k = random.randrange(number_words)
        if test_batch[k][1] == 0 :
            test_batch.pop(k)
            number_words -= 1
        else :
            p = random.randrange(2)
            question = lang[p] + ":\t" + diz_data[test_batch[k][0]][p]
            rightans = diz_data[test_batch[k][0]][not p]
            answer = input("\n" + question + "\n" + lang[not p] + ":\t")
            write_log(question,lang[not p] + ": " + rightans,answer)
            if answer.strip() == rightans :
                diz_data[test_batch[k][0]][2] += 1
                test_batch[k][1] -= 1
            else :
                diz_data[test_batch[k][0]][3] += 1
                test_batch[k][1] += 1
                print("No, the right answer is: " + rightans)
            diz_data[test_batch[k][0]][4]=time.time().__int__()


diz_data = diz_data_upload()
lang = diz_data[0][0:2]
test_batch = choose_batch(diz_data)
testing(test_batch)
diz_data_save(diz_data_file,diz_data)










