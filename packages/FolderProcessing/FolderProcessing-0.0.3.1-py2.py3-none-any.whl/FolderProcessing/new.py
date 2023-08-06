#coding:utf-8
import os

def new(command, path, name, number, Suffix=''):
    """NEW Folder"""
    if command == 'n':
        path_new = path
        name_new = name
        number_new = number
        po = 0
        if int(number) > int(1):
            print("When the file is repeated, a number is added after it")
            for i in range(int(number_new)):
                if int(i) == int(0):
                    os.makedirs(path_new+name_new)
                if int(i) >= int(1):
                    os.makedirs(path_new+name_new+str(i))
                po += 1
                print(f"The first{po} Name is {name_new}")
            print("success!")
        if int(number_new) <= 1:
            os.makedirs(path_new+name_new)
            print(f"The first{number_new} Name is {name_new}")
        print("success!")
    """NEW File"""
    if command == 'n_file':
        path_file = path
        name_file = name
        number_file = number
        Suffix_file = Suffix
        if int(number_file) > int(1):
            print("When the file is repeated, a number is added after it")
            for r in range(int(number_file)):
                if int(r) == int(0):
                    new_files = open(f'{path_file}' f"{name_file}" + str(Suffix_file),"a")
                    new_files.write("")
                    new_files.close()
                if int(r) > int(1):
                    new_files = open(f'{path_file}' f"{name_file}{r}" + str(Suffix_file),"a")
                    new_files.write("")
                    new_files.close()
                print(f"The first{r} Name is {name_file}")
            print("success!")
        if int(number_file) == int(1):
            new_files = open(f'{path_file}' f"{name_file}" + str(Suffix_file),"a")
            new_files.write("")
            new_files.close()
            print(f"The first{number_file} Name is {name_file}")
            print("success!")
