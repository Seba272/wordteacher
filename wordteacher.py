#!/usr/bin/python3
import time
import random
import json
import os
#from os import path
import sys 
from tabulate import tabulate

version = "v2.3"
this_file = "word_teacher_"+version
path_for_wt = "/Users/lupo/.wordteacher/"
#path_for_wt = "/Users/lupo/.wordteacher/dev-datafolder/"
log_file_name = path_for_wt + "wt.log"
log_separator = " ; "

class colors:
    lang = { 0:'\x1b[91m' , 1:'\x1b[94m' }
    std = '\033[0m'

class dizionario:
    #_properties = [ "strategy" , "languages" , "name" , "f_data_name" , "f_info_name" ]
# [[0:lang0, 1:lang1, 2:number of positive tests, 3:number of negative tests, 4:date of inizialization, 5:date of last test],...] 
    def __init__(self,diz_name_in):
        name = "" # Name of dictionary 
        languages = ["",""] # The two languages, padded for display
        strategy = [] # Learning strategy: d1, d2, ... means d1 repetitions first day, d2 the second one...
        f_data_name = "" # path to the file containing the dictionary
        f_info_name = "" # path to the file containing these properties
        birth_date = "" # date of creation of the dictionary
        if diz_name_in == "" :
            print("Upload a new dictionary:")
            self.f_origin_name = input("File containing the dictionary: ").strip()
            if not os.path.exists(self.f_origin_name):
                print("File ",self.f_origin_name," not found.")
                return None
            self.data = []
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
                        a.append(0) # 4: date of first learning
                        a.append(0) # 5: date of last test
                        self.data.append(a)
            lang1 = input("Language 1: ")
            lang2 = input("Language 2: ")
            l = max( len(lang1) , len(lang2) ) + 1
            self.languages = [ lang1.ljust(l) , lang2.ljust(l) ]
#            self.name = lang1 + "-" + lang2
            self.name = input("What name do you give to this dictionary? (no spaces) ")
            self.f_data_name = path_for_wt + self.name + ".wt"
            self.f_info_name = path_for_wt + self.name + ".info"
            strat = input("Which strategy? (format: d1,d2,d3, ... ) ")
            strat = strat.split(",")
            self.strategy = [int(p) for p in strat]
            self.birth_date = int(time.time())
            self.save_data()
            write_log( self.name , "New dictionary opened: " + self.name )
        else:
            self.f_info_name = path_for_wt + diz_name_in + ".info"
            with open( self.f_info_name , "r") as f_info:
                infos = json.load(f_info)
                self.name = infos["name"]
                self.languages = infos["languages"]
                self.strategy = infos["strategy"]
                self.f_data_name = infos["f_data_name"]
                self.f_info_name = infos["f_info_name"]
                self.birth_date = int(infos["birth_date"])
            with open( self.f_data_name , "r") as f_data:
                self.data = json.load(f_data)
            write_log( self.name , "Existing dictionary opened: " + self.name )
    
    def add_word(self,word):
        if self.data[word][0] == "" :
            p = 0 
        elif self.data[word][1] == "" :
            p = 1
        else :
            print("Something went wrong: this word shouldn't be changed.")
            sys.exit()
        newword = input("What is the translation of " + colors.lang[not p] + self.data[word][not p] + colors.std + " in " + colors.lang[p] + self.languages[p] + colors.std + "? ")
        self.data[word][p] = newword

    def save_data(self):
        with open(self.f_data_name,"w") as f_data:
            json.dump(self.data,f_data)
        with open(self.f_info_name,"w") as f_info:
            infos = { \
                    "name" : self.name , \
                    "languages" : self.languages , \
                    "strategy" : self.strategy , \
                    "f_data_name" : self.f_data_name , \
                    "f_info_name" : self.f_info_name , \
                    "birth_date" : self.birth_date \
                    }
            json.dump(infos,f_info)
    
    # [[index in diz, how many repetitions],...]
    def make_batch_learn(self,n_words=5):
        batch = []
        today = int(time.time())
        strat_repetitions = max(self.strategy)
        strat_days = len(self.strategy)
        for w in range(len(self.data)) :
            if self.data[w][4] == 0 :
                word_days = 0
            else :
                word_days = max(int((today/86400 - self.data[w][4]/86400)),0)
            word_level = self.data[w][2] - self.data[w][3]
            if word_days <= strat_days and int(self.data[w][5]/86400) < int(today/86400) : #and word_level < sum([self.strategy[j] for j in range(word_days+1)]) :
                batch.append([w,self.strategy[word_days]])
            if len(batch) >= n_words :
                break
        return batch

    # [[index in diz, how many repetitions],...]
    def make_batch_repeat(self,n_words=5):
        batch = []
        words_active = []
        for w in range(len(self.data)) :
            if self.data[w][2] :
                word_level = self.data[w][3] / self.data[w][2] # value between 0 and 1: the lower the better. We test the ones with largest value.
                words_active.append([w,word_level])
        words_active.sort(key = lambda k: k[1],reverse=True)
        n_words = min(n_words, len(words_active))
        batch = [[words_active[k][0],2] for k in range(n_words)]
        return batch

    def print_status(self):
        print("Name of dictionary: ",self.name)
        print("Database: ",self.f_data_name)
        print("Number of words: ",len(self.data))
        learned_words = 0
        for w in self.data :
            learned_words += ( w[4] != 0 )
        print("Number of words in the learning process: ",learned_words)
        yn = input("Do you want a printout of the whole dictionary? ")
        if yn[0] == "y" :
            f_status_name = input("Where? ")
            header = [self.languages[0], self.languages[1],"Tests","Level","Level","First test","Last test"]
            table = []
            for word in self.data :
                table.append([\
                        word[0],\
                        word[1],\
                        word[2]+word[3],\
                        word[2]-word[3],\
                        word[3]/max(word[2],1),\
                        time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(word[4])),\
                        time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(word[5]))\
                        ])
            with open(f_status_name,"w") as f_status :
                f_status.write(tabulate(table,header))

def write_log(name,string):
    with open(log_file_name,"a") as log_file:
        log_file.write(format(time.time().__int__(),"x"))
        log_file.write(log_separator)
        log_file.write(this_file)
        log_file.write(log_separator)
        log_file.write(name)
        log_file.write(log_separator)
        log_file.write(string)
        log_file.write(" \n")

def testing(test_batch,from_diz,log_string):
    number_words = len(test_batch)
    try:
        while number_words > 0 :
            k = random.randrange(number_words)
            if test_batch[k][1] == 0 :
                test_batch.pop(k)
                number_words -= 1
            else :
                if from_diz.data[test_batch[k][0]][0] == "" or from_diz.data[test_batch[k][0]][1] == "" :
                    from_diz.add_word(test_batch[k][0])
                p = random.randrange(2)
                question = from_diz.data[test_batch[k][0]][p]
                rightans = from_diz.data[test_batch[k][0]][not p]
                answer = input( \
                        colors.lang[p] + from_diz.languages[p] + ": " \
                        + question + "\n"\
                        + colors.lang[not p] + from_diz.languages[not p] + ": ")
                print(colors.std)
                if from_diz.data[test_batch[k][0]][4] == 0 :
                    from_diz.data[test_batch[k][0]][4] = int(time.time())
                from_diz.data[test_batch[k][0]][5] = int(time.time())
                write_log( from_diz.name , log_string + log_separator + question + log_separator + rightans + log_separator + answer)
                if answer.strip() == rightans :
                    from_diz.data[test_batch[k][0]][2] += 1
                    test_batch[k][1] -= 1
                else :
                    from_diz.data[test_batch[k][0]][3] += 1
                    test_batch[k][1] += 1
                    print(colors.std + "No, the right answer is: ", rightans)
    except KeyboardInterrupt:
        print(colors.std)
        pass
    print(colors.std)

def learn(diz):
    length_batch = int(input("How many words? "))
    test_batch = diz.make_batch_learn(length_batch)
    testing(test_batch,diz,"learn")
    diz.save_data()

def repeat(diz):
    length_batch = int(input("How many words? "))
    test_batch = diz.make_batch_repeat(length_batch)
    testing(test_batch,diz,"repeat")
    diz.save_data()

# Menu
print("== Word Teacher ",version," ==")
while 1:
    print("What do you want to do?")
    print("0. Upload a new dictionary")
    files = os.listdir(path_for_wt)
    dictionaries = []
    k = 1
    for f in files:
        ff = f.split(".")
        if ff[-1] == "wt" :
            dictionaries.append(ff[-2])
            print( str(k)+". Use ", ff[-2] )
            k+=1
    print("q. Exit")
    ans = input()
    if ans == "q" :
        sys.exit()
    try:
        ans = int(ans)
    except ValueError :
        print("There is not such option.")
        continue
    if ans == 0 :
        diz_name_in = "" # input("Which diz_name?")
    elif ans <= len(dictionaries) :
        diz_name_in = dictionaries[ans-1]
    else :
        print("There is not such an option.")
        continue
    diz = dizionario(diz_name_in)
    if diz.name == "" :
        print("Something went wrong. Try again!")
        continue
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
            learn(diz)
        elif ans == "2":
            repeat(diz)
        elif ans == "3":
            diz.print_status()
        else:
            print("There is not such option.")
            continue














