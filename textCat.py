#!/usr/bin/python3
from cmath import log
from collections import defaultdict
import os
import re

r = re.compile("(^|[^a-zA-Z0-9_\n])([a-zA-Z_]+)", re.MULTILINE)
def tokenize(s): # TODO better tokenization
    global r
    m = r.findall(s)
    return [mi for _,mi in m] 


class Trainer: 
    '''
        Naive Bayse trainer 
    '''
    def __init__(self, train_data_location=None):
        if train_data_location is not None: 
            self.train_data_location = train_data_location
        else: 
            print("input training data location")
            self.train_data_location = input()

        self.Pc = defaultdict(lambda : 0)
        self.Ptgc = defaultdict(lambda : defaultdict(lambda : 0))
        self._train(); 
        

    def _train(self):
        # build Pc and Ptgc
        with open(self.train_data_location, 'r') as lst:
            for line in lst:
                [path,answer] = line.split(" ")
                path = f"{os.path.dirname(self.train_data_location)}/{path}"
                self.Pc[answer] += 1
                with open(path, 'r') as doc:
                    docStr = doc.read()
                    for w in tokenize(docStr):  
                        self.Ptgc[w][answer] += 1
            
class Tester: 

    def __init__(self,input_file_name=None, output_file_name=None, trainer=None):
        self.trainer = trainer if trainer is not None else Trainer()
        if input_file_name is None:
            print("Insert unlabled input file")
            self.input_file_name = input()
        else: 
            self.input_file_name = input_file_name

        self.data = defaultdict(lambda : "Unkown")
        with open(self.input_file_name, 'r') as lst:
            for path in lst: 
                self._test(f"{os.path.dirname(self.input_file_name)}/{path[:-1]}")

        if output_file_name is None:
            print("Insert labled output file")
            self.output_file_name = input()
        else: 
            self.output_file_name = output_file_name
        self._output()
    

    def _test(self,path):
        with open(path, 'r') as doc: 
            ts = tokenize(doc.read())
            args = defaultdict(lambda : 0)
            for c,val in self.trainer.Pc.items():
                val = 0
                for t in ts:
                    val += log(self.trainer.Ptgc[t][c] + 1)
                args[c] = log(val) + val
            self.data[path] = max(args)
    
    def _output(self):
        with open(self.output_file_name, 'w') as output:
            for path,answer in self.data.items():
                output.write(f"{path} {answer}")

 
if __name__ == "__main__":
    t = Tester("./TC_provided/corpus1_test.list","./out.labels", Trainer("./TC_provided/corpus1_train.labels")); 