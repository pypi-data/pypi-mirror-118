#!/usr/bin/env python3
# fileops.py


import os

def readFile(path):
    if os.path.exists(path):
        return [{"file": "contents"}]
    else:
        print("File does not exist")
        return ''



def main():
    pass

if __name__ == '__main__':
    main()

