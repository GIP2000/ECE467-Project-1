#!/usr/bin/python3
from textCat import Trainer, Tester
from make_TT_pair import make_split
from collections import defaultdict

def validate(filename,p_data):
    correct = 0
    incorrect = 0
    with open(filename, 'r') as file:
        for line in file: 
            [name,value] = line.split(" ")
            correct += (p_data[name] == value)
            incorrect += (p_data[name] != value)
    return (correct/(correct+incorrect))
            

def stepper(inputFile,testFile,validatorFile ):
    step = .001
    i = step
    vals = []
    train = Trainer(inputFile)
    while i < .07:
        # print(f"starting with smoothing_factor = {i}")
        test = Tester(testFile,"./out.txt",train,True,False,i)
        vals.append(validate(validatorFile,test.data))
        # print(f"value for smf {i} = {vals[-1]}")
        i+= step
    
    # largestVal = 0; 
    # largestIndex = 0; 
    # for i,val in enumerate(vals):
    #     if val > largestVal:
    #         largestVal = val
    #         largestIndex = i
    # print(f"largest alpha {(largestIndex+1) *.001} largest Val {largestVal}")
    # print(f"alhpa = .01 val = {vals[9]}")
    
    # return (largestIndex, largestVal)
    return vals

if __name__ == "__main__":
    steps = 50
    # inputFile = input("Input training file path: ")
    # testFile = input("Input test list file path: ")
    # validatorFile = input("Input validator label file: ")
    make_split("./TC_provided/corpus3_train.labels")
    inputFile = "./TC_provided/new_train.labels"
    testFile = "./TC_provided/new_test.list"
    validatorFile = "./TC_provided/new_test.labels"
    vals = defaultdict(lambda : 0)
    avg_p = defaultdict(int)
    for i in range(0,steps):
        print(f"trial {i} starting")
        make_split("./TC_provided/corpus3_train.labels")
        t_vals = stepper(inputFile,testFile,validatorFile)
        vals = [a+b for a,b in zip(vals,t_vals)] if len(vals) == len(t_vals) else t_vals
    
    
    ma = 0
    mi = 0
    for i,val in enumerate(vals):
        avg = val/steps
        print(f"alpha {(i+1)*.001}|| avg {avg}")
        if avg > ma:
            ma = avg
            mi = i
    
    print(f"best avg alpha {(ma+1)*.001} with avg alpha {ma}")

    


    # .097 corpus 1 
    # .001 corpus 2 .04
    # .022 corpus 3 .014



    #prob = log((wc_in_cat + alpha)/(documents in cat + cat_amount*alpha))
