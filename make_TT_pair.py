#!/usr/bin/python3
from sys import argv

if __name__ == "__main__":
    if len(argv) != 3:
        print("usage ./make_TT_pair.py <training file name> <int(1-4) which quarter to cut off>")
        exit(1)
    
    [_,path,quarter] = argv
    quarter = int(quarter) 

    with open(path, 'r') as lst, open("./TC_provided/new_train.labels", 'w') as train, open("./TC_provided/new_test.labels", 'w') as test_label, open("./TC_provided/new_test.list", 'w') as test_list:
        lines = [line.strip("\n") for line in lst if line != "\n"]
        linecount = len(lines)
        for i,line in enumerate(lines):
            if i/linecount < .25*quarter and i/linecount > .25*(quarter-1) :
                test_label.write(f"{line}\n")
                path = line.split(' ')[0]
                test_list.write(f"{path}\n")
            else:
                train.write(f"{line}\n")