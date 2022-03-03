#!/usr/bin/python3
from textCat import Trainer, Tester

def validate(filename,p_data):
    correct = 0
    incorrect = 0
    with open(filename, 'r') as file:
        for line in file: 
            [name,value] = line.split(" ")
            correct += (p_data[name] == value)
            incorrect += (p_data[name] != value)
    return (correct/(correct+incorrect))
            
    

if __name__ == "__main__":
    inputFile = input("Input training file path: ")
    testFile = input("Input test list file path: ")
    validatorFile = input("Input validator label file: ")

    step = .001
    i = step
    vals = []
    train = Trainer(inputFile)
    while i < .15:
        print(f"starting with smoothing_factor = {i}")
        test = Tester(testFile,"./out.txt",train,True,False,i)
        vals.append(validate(validatorFile,test.data))
        print(f"value for smf {i} = {vals[-1]}")
        i+= step
    
    largestVal = 0; 
    largestIndex = 0; 
    for i,val in enumerate(vals):
        if val > largestVal:
            largestVal = val
            largestIndex = i

    print(f"The best value is {(largestIndex+1)*step}")


    # .082 corpus 1 
    # .001 corpus 2 
    # .037 corpus 3 



    #prob = log((wc_in_cat + alpha)/(documents in cat + cat_amount*alpha))
