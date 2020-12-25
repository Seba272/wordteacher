#!/usr/bin/python3
import time

log_file = "wt.log"
log_separator = " ; "

def write_log(qst,ans_c,ans):
    with open(log_file,"a") as fl:
        fl.write(format(time.time().__int__(),"x"))
        fl.write(log_separator)
        fl.write("word teacher 01.1")
        fl.write(log_separator)
        fl.write(qst)
        fl.write(log_separator)
        fl.write(ans_c)
        fl.write(log_separator)
        fl.write(ans)
        fl.write(" \n")

diz_file="dict"
diz_data=[]

def diz_upload(f=diz_file):
    dd = []
    with open(f,"r") as fd:
        for line in fd:
            if line[0]=="%":
                continue
            a = line.strip().split(";")
            dd.append(a)
    return dd

diz_data = diz_upload()

for test in diz_data:
    question = test[0]
    rightans = test[1]
    answer = input(question + '\n\t')
    write_log(question,rightans,answer)


#k = 0
#for k in range(5) :
#    question = "Cosa è " + str(k) + " a parole?"
#    answer = input(question + '\n\t')
#    write_log(question,answer)

print("fatto")



