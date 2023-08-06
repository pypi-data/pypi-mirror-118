#!/usr/bin/env python3
# fileOps.py


import os

def readFile(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.readlines()
            f.close()
            return content
    else:
        print("File does not exist")
        return ''

def writeFile(path, inputString):
    try:
        with open(path, "w") as f:
            content = f.readlines()
            f.write(inputString)
            return content
    except Exception as e:
        print("ERROR: "+str(e))
        exit(1)

def appendFile(path, inputString):
    try:
        with open(path, "a") as f:
            content = f.readlines()
            f.write(inputString)
            return content
    except Exception as e:
        print("ERROR: "+str(e))
        exit(1)


def main():
    pass

if __name__ == '__main__':
    main()

