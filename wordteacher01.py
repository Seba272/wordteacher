#!/usr/bin/python3
import time
import random
import json
from os import path

log_file = "wt.log"
log_separator = " ; "

def write_log(qst,ans_c,ans):
    with open(log_file,"a") as fl:
        fl.write(format(time.time().__int__(),"x"))
        fl.write(log_separator)
        fl.write("word teacher 01.2")
        fl.write(log_separator)
        fl.write(qst)
        fl.write(log_separator)
        fl.write(ans_c)
        fl.write(log_separator)
        fl.write(ans)
        fl.write(" \n")

diz_file="dict"
diz_data=[] 
# [[0:lang0, 1:lang1, 2:number of positive tests, 3:number of negative tests, 4:date of last test],...]

def diz_upload(f=diz_file):
    dd = []
    with open(f,"r") as fd:
        for line in fd:
            if line[0]=="%":
                continue
            if line[0]=="!":
                #line = line[1:].strip().replace(" ","")
                line = line[1:]
                #line = lang.split(";")
            a = line.split(";")
            a = [b.strip() for b in a]
            a.append(0)
            a.append(0)
            a.append(0)
            dd.append(a)
    return dd

def testing(test_batch):
    for test in test_batch:
        p = (random.random() < 1/2) 
        question = lang[p] + ":\t" + diz_data[test][p]
        rightans = diz_data[test][not p]
        answer = input("\n" + question + "\n" + lang[not p] + ":\t")
        write_log(question,lang[not p] + ": " + rightans,answer)
        if answer.strip()==rightans :
            diz_data[test][2]+=1
        else :
            diz_data[test][3]+=1
            print("No, the right answer is: " + rightans)
        diz_data[test][4]=time.time().__int__()

diz_data_file = "diz_data_file2"

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

def choose_batch(dd=diz_data):
    return range(1,len(diz_data))


diz_data = diz_data_upload()
lang = diz_data[0][0:2]
#lang = [ "Italiano", "Deutsch"]
test_batch = choose_batch(diz_data)
testing(test_batch)
diz_data_save(diz_data_file,diz_data)






#k = 0
#for k in range(5) :
#    question = "Cosa è " + str(k) + " a parole?"
#    answer = input(question + '\n\t')
#    write_log(question,answer)




