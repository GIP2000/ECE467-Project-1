#!/usr/bin/python3
from cmath import log
from collections import defaultdict
from os.path import dirname
from functools import reduce 
from nltk import download as nltk_download
nltk_download("stopwords")
nltk_download("punkt")
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))

def tokenize(s):
    return [w for w in word_tokenize(s) if (w not in stop_words and w.isalpha())]

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


class Tester: 
    '''
        Naive Bayes Tester
    '''

    def __init__(self,input_file_name=None, output_file_name=None, trainer=None, batch_prediction=True, outputToFile=True, sf = None):
        self.trainer = trainer if trainer is not None else Trainer()
        if not batch_prediction: 
            return
        
        # Pick the smoothing factor
        if sf is not None:
            self.sf = sf
        else:
            if "Pol\n" in self.trainer.Pc or "Pol" in self.trainer.Pc :
                self.sf = .097
            elif "I\n" in self.trainer.Pc or "I" in self.trainer.Pc :
                self.sf = .0118
            elif "Wor\n" in self.trainer.Pc or "Wor" in self.trainer.Pc :
                self.sf = .062
            else:
                self.sf = .082


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
    t = Tester()