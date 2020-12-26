#!/usr/bin/python3
import time
import random
import json
import os
#from os import path
import sys 
from tabulate import tabulate

this_file = "word_teacher_v1.1"
log_file = "wt.log"
log_separator = " ; "

class dizionario:
    strategy = [2,2,2,2,2]
    
    def __init__(self,theme):
        #nonlocal self.data, self.theme
        self.theme = theme
        self.languages = theme.split("-")
        self.f_origin_name = self.theme + ".csv"
        self.f_data_name = "." + self.theme + ".wt"
        self.data = []
# [[0:lang0, 1:lang1, 2:number of positive tests, 3:number of negative tests, 4:date of inizialization, 5:date of last test],...]
        if os.path.exists(self.f_data_name):
            with open(self.f_data_name, "r") as f_data:
                self.data = json.load(f_data)
        elif os.path.exists(self.f_origin_name):
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
    
    # [[index in diz, how many repetitions],...]
    def make_batch_learn(self,n_words=5):
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

    # [[index in diz, how many repetitions],...]
    def make_batch_repeat(self,n_words=5):
        batch = []
        words_active = []
        for w in range(len(self.data)) :
            word_touched = self.data[w][2] + self.data[w][3]
            word_level = self.data[w][2] - self.data[w][3]
            if word_touched != 0 :
                words_active.append([w,word_level])
        words_active.sort(key = lambda k: k[1])
        batch = [[words_active[k][0],2] for k in range(n_words)]
        return batch

    def print_status(self):
        print("Name of dictionary: ",self.theme)
        print("File of origin: ",self.f_origin_name)
        print("Database: ",self.f_data_name)
        print("Number of words: ",len(self.data))
        yn = input("Do you want a printout of the whole dictionary? ")
        if yn == "y" or yn == "yes" :
            f_status_name = input("Where?")
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
            with open(f_status_name,"w") as f_status :
                f_status.write(tabulate(table,header))

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
                print("No, the right answer is: ", rightans)
            from_diz.data[test_batch[k][0]][5] = int(time.time())

def learn():
    length_batch = int(input("How many words? "))
    test_batch = diz.make_batch_learn(length_batch)
    testing(test_batch,diz)
    diz.save_data()

def repeat():
    length_batch = int(input("How many words? "))
    test_batch = diz.make_batch_repeat(length_batch)
    testing(test_batch,diz)
    diz.save_data()

# Menu
while 1:
    print("What do you want to do?")
    print("0. Upload a new dictionary")
    files = os.listdir(".")
    dictionaries = []
    for f in files:
        a = f.split(".")[-1]
        if a == "wt" :
            dictionaries.append(f)
    k = 1
    for f in dictionaries:
        ff = f.split(".")[-2]
        print(str(k)+". Use ",ff)
        k+=1
    print("q. Exit")
    ans = input()
    if ans == "q" :
        sys.exit()
    ans = int(ans)
    if ans == 0:
        theme = input("Which theme?")
    elif ans <= len(dictionaries) :
        theme = dictionaries[ans-1].split(".")[-2]
    else :
        print("There is not such option.")
        continue
    diz = dizionario(theme)
    while 1:
        print("What do you want to do?")
        print("1. Go on with learning")
        print("2. Repeat learned words")
        print("3. Print out status of dictionary")
        print("q. Return to main menu")
        ans = input()
        if ans == "q":
            break
        elif ans == "1":
            learn()
        elif ans == "2":
            repeat()
        elif ans == "3":
            diz.print_status()
        else:
            print("There is not such option.")
            continue














