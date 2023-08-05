#-*- coding:utf-8 -*-
class OS:
    def __init__(self, message, file=r''):
        self.message = message
        self.file = file
    
    def OsList(self):
        if self.message == 'help' or self.message == '':
            print("=========================================================================================="\
                  "\nFolder Processing"\
                  "\n--------------------"\
                  "\nfrom FolderProcessing import view "\
                  "\n--------------------------------------"\
                  "\n命令：view.OS('{file:命令输出位置文件夹所有文件}', '{文件地址如：C:\\xxx\\xxx\\xxx}')"\
                  "\n-----------------------------------------------------------------------------------------"\
                  "\nview.OS.OsList()#配合 file命令 "\
                  "\n---------------------------------")
        if self.message == 'file':
            import os
            import re
            import glob
            filePath = (f'{self.file}')
            if self.file == '':
                return
            os.listdir(filePath)
            number = 0
            for i,j,k in os.walk(filePath):
                number += 1
                print(f"\n\t第{number}个文件夹",i,j,k)
            print(f"\n\n所有文件如上,共{number}个文件夹")
