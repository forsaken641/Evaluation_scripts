import json
from class1 import *
token="sgp_local_8876a7d89fa0bf4936b9f5eae6dcb08f50ee9295"
from script import *
import time

def locatefunc(varline,funcs):
    num=len(funcs)
    if num==0:
        return -1
    func=funcs[num//2]
    if varline<=func[1] and varline >=func[0]:
        return num//2
    elif varline<func[0]:
        return locatefunc(varline,funcs[:num//2])
    else:
        return locatefunc(varline,funcs[num//2+1:])+num//2

def get_funcname(jsonfile,projecthash=''):

    result={
        "repo":"",
        "patch_hash":"",
        "vul_hash":"",
        "result":{}
    }

    with open(jsonfile,'r') as f:
        content = json.load(f)
    if not projecthash:
        projecthash=content["vul_hash"]
    projectname=content["repo"].split('/')[1]
    oldfiles=content["line_dict"]["old"]
    result["repo"]="repo:^"+projectname+"$@"+projecthash
    result["patch_hash"]=content["patch_hash"]
    result["vul_hash"]=content["vul_hash"]
    for oldfile in oldfiles:
        result["result"][oldfile]=[]
        query="context:global repo:^"+projectname+"$ rev:@master:"+projecthash+" file:"+oldfile
        print(query)
        test=Content(projectname,query,"file",token)
        data=test.get_result()
        with open("./temp.c",'w',encoding='gb18030') as tempfile:
            tempfile.write(data)
        funcs=get_func("./temp.c")
        #print(funcs)
        vars=oldfiles[oldfile]
        for var in vars:
            varline=var[0]
            varname=var[1]
            num=locatefunc(varline,funcs)
            if num!=-1:
                if result["result"][oldfile] and funcs[num][3]==result["result"][oldfile][-1]['name']:
                    type="func"
                    result["result"][oldfile][-1]["key_variables"].append(tuple([varline,varname]))

                else:
                    type = "func"
                    result["result"][oldfile].append({"type": type,
                                                      "name": funcs[num][3],
                                                      "line_range": [funcs[num][0], funcs[num][1]],
                                                      "source_code": funcs[num][2],
                                                      "key_variables": [tuple([varline, varname])]
                                                      }
                                                     )
            else:
                type="block"
                result["result"][oldfile].append({"type": type,
                                                  "name": 'block',
                                                  "line_range": '',
                                                  "source_code": '',
                                                  "key_variables": tuple([varline, varname])
                                                  }
                                                 )
                time.sleep(0.01)
    return result
            #print(funcname)


if __name__ == "__main__":
    result=get_funcname('./json/awtk-version-1.7.0.json','4de4a37')
    #print(result)
    json_str=json.dumps(result)
    with open('./json/result.json','w') as f:
        json.dump(result,f,indent=3,ensure_ascii=False)