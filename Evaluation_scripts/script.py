import os
import openpyxl
from get_source_by_gpt import *
from tree_sitter import Language, Parser
from io import StringIO

#groundtruth
xlsxpath="..\\测试数据\\test.xlsx"
#待测软件所在路径
database="..\\database\\"


#得到函数名及起始和终止行号
def get_func(filename):
    Language.build_library(
        'build/my-languages.so',
        [
            './tree-sitter-cpp'
        ]
    )
    CPP_LANGUAGE = Language('build/my-languages.so', 'cpp')

    parser = Parser()
    parser.set_language(CPP_LANGUAGE)


    file=open(filename,'r')
    code = StringIO(file.read()).read()

    tree = parser.parse(bytes(code, "utf-8"))
    root_node = tree.root_node
    comments = []
    functions = []
    # 为了确定起始行
    code = code.split("\n")
    for child_node in root_node.children:
        if child_node.type == "function_definition":
            function_start_line = child_node.start_point[0]
            function_end_line = child_node.end_point[0]
            # 不在同一行
            if function_start_line != function_end_line:
                function_code = code[function_start_line:function_end_line + 1]
                function_code = "\n".join(function_code)
            else:
                function_code = code[function_start_line]
                # 起始行列  终止行列 函数代码 函数名

            functions.append([child_node.start_point[0], child_node.end_point[0], function_code,code[function_start_line].split('(')[0].split(' ')[-1]])
    return functions


def get_gt(path):
    wb = openpyxl.load_workbook(path)
    ws=wb.active
    list1=[]
    for row in ws.iter_rows():
        if(row[0].value=="id"):
            continue
        list1.append({
            "CVE":row[0].value,
            "line_num":row[5].value,
            "statement":row[8].value,
            "filename":row[4].value,
            "fucname":row[7].value,
            "software":row[3].value,
            "hash":row[1].value
        })
    return list1
#value为单个CVE样例生成的结果,gt为对应CVE的groundtruth,basenum为代码片段的起始行号
def compare(gt,value,basenum):
    for v in value:
        if v['statement'].find(gt['statement'])!=-1 and v['line_num']+basenum-1==gt['line_num']:
            return True
    return False




if __name__ == "__main__":
    list1=get_gt(xlsxpath)
    total=0
    score=0
    for gt in list1:
        #print(gt)
        path=database+gt["software"]
        os.chdir(path)

        print("git checkout -f " + gt["hash"])
        os.system("git checkout -f " + gt["hash"])
        os.chdir("D:\\leak\\智能漏洞检测\\CWE-476\\规则\\Evaluation_scripts")
        filename=path+"\\"+gt['filename']
        funcs = get_func(filename)
        temp=[]
        prompt=''
        for func in funcs:
            if func[3].find(gt['filename'])!=-1:
                prompt = creat_message(
                    filename,
                    func[0], func[1])
                temp=func
                break
        list_msg = []
        list_msg.append({"role": "user", "content": prompt})
        res = generate_response(list_msg)
        #print(res['choices'][0]['message']['content'])
        if compare(gt,res,func[0]):
            score=score+1
        total=total+1

