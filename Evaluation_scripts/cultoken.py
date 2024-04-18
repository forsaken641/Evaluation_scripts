# -*- coding: utf-8 -*-
from parse_getout_nearfunc_c_plus import *
import tiktoken
import json
import os
from  script import *

datapath="D:\\leak\\智能漏洞检测\\CWE-476\\t113-system-prj\\"

# 计算输入消耗的token数量
def num_tokens_from_string(string: str, encoding_name: str) -> int:
 """Returns the number of tokens in a text string."""
 encoding = tiktoken.get_encoding(encoding_name)
 num_tokens = len(encoding.encode(string))
 return num_tokens

def findfile(pathName):
    filelist=[]
    if os.path.exists(pathName):
        fileList = os.listdir(pathName) #当前目录列表
        for f in fileList:
            if f == "$RECYCLE.BIN" or f == "System Volume Information":
                continue
            fpath = os.path.join(pathName, f)
            if os.path.isdir(fpath):
                fpath=fpath+"/"
                filelist=filelist+findfile(fpath)
            else:
                if fpath.endswith('.c') or fpath.endswith('.cpp'):
                    filelist.append(fpath)
        return filelist

if __name__ == "__main__":
    filelist=findfile(datapath)
    totol=0
    unable=0
    for file in filelist:
        #print(file)
        content=get_func(file)
        if content:
            for str in content:
                if str:
                    #print(str[2])
                    totol=totol+num_tokens_from_string(str[2],"cl100k_base")
        else:
            unable=unable+1
            print(file)
            continue
    print("totol",totol)
    print(unable)