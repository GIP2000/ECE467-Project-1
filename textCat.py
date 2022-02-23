#!/usr/bin/python3
from cmath import log
from collections import defaultdict
from os.path import dirname
import re
from functools import reduce 

def tokenize(s):
    r = re.compile("(^|[^a-zA-Z0-9_\n])([a-zA-Z_]+)", re.MULTILINE)
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

        self.smoothing_factor = .07
        self.Pc = defaultdict(lambda : 0)
        self.Ptgc = defaultdict(lambda : defaultdict(lambda : self.smoothing_factor))
        self.unique_tokens = set()
        self._train(); 
        

    def _train(self):
        # build Pc and Ptgc
        with open(self.train_data_location, 'r') as lst:
            self.doc_count = 0
            for line in lst:
                self.doc_count+=1
                [path,answer] = line.split(" ")
                path = f"{dirname(self.train_data_location)}/{path}"
                self.Pc[answer] += 1
                with open(path, 'r') as doc:
                    docStr = doc.read()
                    for w in tokenize(docStr):  
                        self.Ptgc[w][answer] += 1
                        self.unique_tokens.add(w)


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
                self._test(f"{dirname(self.input_file_name)}/{path[:-1]}",path[:-1])

        if output_file_name is None:
            print("Insert labled output file")
            self.output_file_name = input()
        else: 
            self.output_file_name = output_file_name
        self._output()
    

    def _test(self,path,rpath):
        with open(path, 'r') as doc: 
            ts = tokenize(doc.read())
            args = {c:log(val/self.trainer.doc_count) + reduce(lambda y,t:y+log(self.trainer.Ptgc[t][c]/val) ,ts,0) for (c,val) in self.trainer.Pc.items()}
            self.data[rpath] = reduce(lambda acc,x: x if args[x].real > args[acc].real else acc ,args)
    
    def _output(self):
        with open(self.output_file_name, 'w') as output:
            for path,answer in self.data.items():
                output.write(f"{path} {answer}")

 
if __name__ == "__main__":
    t = Tester("./TC_provided/corpus1_test.list","./out.labels", Trainer("TC_provided/corpus1_train.labels")); 
    # Tester(); 