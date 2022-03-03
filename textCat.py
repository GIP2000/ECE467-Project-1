#!/usr/bin/python3
from cmath import log
from collections import defaultdict
from os.path import dirname
from re import compile as re_compile, MULTILINE as RMULTILINE
from functools import reduce 

def tokenize(s):
    r = re_compile("(^|[^a-zA-Z0-9_\n])([a-zA-Z_]+)", RMULTILINE)
    m = r.findall(s)
    return [mi for _,mi in m]

def validate(filename,p_data):
    correct = 0
    incorrect = 0
    with open(filename, 'r') as file:
        for line in file: 
            [name,value] = line.split(" ")
            correct += (p_data[name] == value)
            incorrect += (p_data[name] != value)
    return (correct/(correct+incorrect))


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

        # self.smoothing_factor = smoothing_factor
        self.Pc = defaultdict(lambda : 0)
        self.Ptgc = defaultdict(lambda : defaultdict(lambda : 0))
        # self.unique_tokens = set()
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
                    used_words = []
                    docStr = doc.read()
                    for w in tokenize(docStr):  
                        if w not in used_words:
                            self.Ptgc[w][answer] += 1
                            used_words.append(w)
                        # self.unique_tokens.add(w)


class Tester: 

    def __init__(self,input_file_name=None, output_file_name=None, trainer=None, batch_prediction=True, outputToFile=True, sf = .08):
        self.sf = sf
        print(self.sf)
        self.trainer = trainer if trainer is not None else Trainer()
        if not batch_prediction: 
            return

        if input_file_name is None:
            print("Insert unlabled input file")
            self.input_file_name = input()
        else: 
            self.input_file_name = input_file_name

        self.data = defaultdict(lambda : "Unkown")
        self._test()

        if output_file_name is None:
            print("Insert labled output file")
            self.output_file_name = input()
        else: 
            self.output_file_name = output_file_name
        if outputToFile: 
            self._output()
    
    def _test(self):
        with open(self.input_file_name, 'r') as lst:
            for path in lst: 
                with open(f"{dirname(self.input_file_name)}/{path[:-1]}", 'r') as doc: 
                    self.predict(doc.read(),path[:-1])
    
    def predict(self,str,name):
        assert name not in self.data
        ts = tokenize(str)
        args = {c:log(d_in_cat/self.trainer.doc_count) + reduce(lambda acc,t:acc+log(((self.trainer.Ptgc[t][c] + self.sf)/(d_in_cat + (len(self.trainer.Pc)*self.sf)))) ,ts,0) for (c,d_in_cat) in self.trainer.Pc.items()}
        self.data[name] = reduce(lambda acc,x: x if args[x].real > args[acc].real else acc ,args) # get max arg c
        return self.data[name]

    
    def _output(self):
        with open(self.output_file_name, 'w') as output:
            for path,answer in self.data.items():
                output.write(f"{path} {answer}")

 
if __name__ == "__main__":
    # t = Tester("./TC_provided/corpus1_test.list","./out.labels", Trainer("TC_provided/corpus1_train.labels"), sf=.115); 
    t = Tester("./TC_provided/new_test.list","./out.labels", Trainer("TC_provided/new_train.labels"),sf=.037); 
    # t = Tester()
    print(validate("./TC_provided/new_test.labels", t.data))