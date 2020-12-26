#!/usr/bin/python3
import time
import random
import json
from os import path
import sys 
from tabulate import tabulate

this_file = "word_teacher_v1.0"
log_file = "wt.log"
log_separator = " ; "

class dizionario:
#    self.theme = theme
    strategy = [2,2,2,2,2]
    #theme = f_origin.split(".")[0]
    #f_data_name = "." + theme + ".wt"
    
    def __init__(self,theme):
        #nonlocal self.data, self.theme
        self.theme = theme
        self.languages = theme.split("-")
        self.f_origin_name = self.theme + ".csv"
        self.f_data_name = "." + self.theme + ".wt"
        self.data = []
        if path.exists(self.f_data_name):
            with open(self.f_data_name, "r") as f_data:
                self.data = json.load(f_data)
        elif path.exists(self.f_origin_name):
            with open(self.f_origin_name,"r") as f_origin:
                today = int(time.time())
                for line in f_origin:
                    if line[0]=="%":
                        continue
                    if line[0]=="!":
                        continue
                    a = line.split(";")
                    a = [b.strip() for b in a]
                    a.append(0) # 2: positive tests
                    a.append(0) # 3: negative tests
                    a.append(today) # 4: date of inizialization
                    a.append(0) # 5: date of last test
                    self.data.append(a)
        else:
            print("No dictionary ",self.f_origin_name," found.\n Terminated.")
            sys.exit("No dictionary found.")
    
    def save_data(self):
        with open(self.f_data_name,"w") as f_data:
            json.dump(self.data,f_data)
    
    # [[index in diz,level],...]
    def make_batch(self,n_words=5):
        batch = []
        today = int(time.time())
        strat_repetitions = max(self.strategy)
        strat_days = len(self.strategy)
        for w in range(len(self.data)) :
            word_days = max(int((self.data[w][5]-today)/86400),0)
            word_level = self.data[w][2] - self.data[w][3]
            if word_days < strat_days and word_level < sum([self.strategy[j] for j in range(word_days+1)]) :
                batch.append([w,self.strategy[word_days]])
            if len(batch) >= n_words :
                break
    #    print("choose_batch: a:\n",a)
        return batch

    def print_status(self):
        print("Name of dictionary: ",self.theme)
        print("File of origin: ",self.f_origin_name)
        print("Database: ",self.f_data_name)
        print("Number of words: ",len(self.data))
        yn = input("Do you want a printout of the dictionary? ")
        if yn == "y" or yn == "yes" :
            header = [self.languages[0],self.languages[1],"Tests","Level","When uploaded","Last tested"]
            table = []
            for word in self.data :
                table.append([\
                        word[0],\
                        word[1],\
                        word[2]+word[3],\
                        word[2]-word[3],\
                        time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(word[4])),\
                        time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(word[5]))\
                        ])
            print(tabulate(table,header))
        
    
#    def diz_upload(f=diz_file):
#        dd = []
#        today = int(time.time())
#        with open(f,"r") as fd:
#            for line in fd:
#                if line[0]=="%":
#                    continue
#                if line[0]=="!":
#                    line = line[1:]
#                a = line.split(";")
#                a = [b.strip() for b in a]
#                a.append(0) # 2: positive tests
#                a.append(0) # 3: negative tests
#                a.append(today) # 4: date of inizialization
#                a.append(0) # 5: date of last test
#                dd.append(a)
#        return dd
    
#    def diz_data_save(f=diz_data_file,dd=diz_data):
#        with open(f,"w") as fl:
#            json.dump(dd,fl)
    
#    def diz_data_upload(f=diz_data_file,dd=diz_data):
#        if path.exists(diz_data_file):
#            with open(diz_data_file, "r") as fup:
#                dd = json.load(fup)
#        else:
#            dd = diz_upload()
#        return dd
    
    # [[index in diz,level],...]
#    def choose_batch(dd=diz_data,n_words=5):
#        a = []
#        today = int(time.time())
#        strat_repetitions = max(strat_exercise)
#        strat_days = len(strat_exercise)
#    #    print("choose_batch: diz_data, dd: \n",dd)
#    #    print("choose_batch: today \n",today)
#        for w in range(1,len(dd)) :
#            word_days = max(int((dd[w][5]-today)/86400),0)
#            word_level = dd[w][2]-dd[w][3]
#    #        print("choose_batch: w=",w,"; word_days=",word_days,"; word_level=",word_level,"; strat_days=",strat_days,"; sum=",sum([strat_exercise[j] for j in range(word_days)]),"; k=",k,"\n")
#            if word_days < strat_days and word_level < sum([strat_exercise[j] for j in range(word_days+1)]) :
#                a.append([w,strat_exercise[word_days]])
#            if len(a) >= n_words :
#                break
#    #    print("choose_batch: a:\n",a)
#        return a
    

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
def testing(test_batch,from_diz):
    number_words = len(test_batch)
    while number_words > 0 :
        k = random.randrange(number_words)
        if test_batch[k][1] == 0 :
            test_batch.pop(k)
            number_words -= 1
        else :
            p = random.randrange(2)
            question = from_diz.languages[p] + ":\t" + from_diz.data[test_batch[k][0]][p]
            rightans = from_diz.data[test_batch[k][0]][not p]
            answer = input("\n" + question + "\n" + from_diz.languages[not p] + ":\t")
            write_log(question,from_diz.languages[not p] + ": " + rightans,answer)
            if answer.strip() == rightans :
                from_diz.data[test_batch[k][0]][2] += 1
                test_batch[k][1] -= 1
            else :
                from_diz.data[test_batch[k][0]][3] += 1
                test_batch[k][1] += 1
                print("No, the right answer is: " + rightans)
            from_diz.data[test_batch[k][0]][5]=time.time().__int__()

theme = input("Which theme? ")
length_batches = int(input("How many words? "))
diz = dizionario(theme)
#lang = diz.languages
test_batch = diz.make_batch(length_batches)
#testing(test_batch,diz)
diz.save_data()
diz.print_status()










