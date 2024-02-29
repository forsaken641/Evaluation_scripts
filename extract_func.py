import pickle
import os
import json
import pandas
from tqdm import tqdm
from datasets import load_dataset
from functools import partial

def read_func(filename,linenumber,linenumberEnd):
    
    with open(filename,'r')as f:
        lines = f.readlines()
    code=""
    for line in lines[linenumber-1:linenumberEnd]:
        code = code+line
    return code

def extract_specific_project(dataset='starcoder'):
    project_dirs=[('/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code','/home/ubuntu/Pseudo-Labelling/json/final copy.json')]
        # ('/home/ubuntu/Pseudo-Labelling/Bochs-REL_2_6_2_FINAL','/home/ubuntu/Pseudo-Labelling/bochs_funcs.json'),
        #           ('/home/ubuntu/Pseudo-Labelling/gstreamer-0.10','/home/ubuntu/Pseudo-Labelling/gstreamer_funcs.json'),
        #           ('/home/ubuntu/Pseudo-Labelling/libav-0.8.10','/home/ubuntu/Pseudo-Labelling/libav_funcs.json'),
        #           ('/home/ubuntu/Pseudo-Labelling/xen-stable-4.0','/home/ubuntu/Pseudo-Labelling/xen_funcs.json')]
    if dataset=='starcoder':
        project_dirs=[('/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code',[os.path.join('/home/ubuntu/Pseudo-Labelling/json',str(i),'final.json')for i in range(8)])]
    final=[]
    index=0
    for project_root, json_files in project_dirs:
        for json_file in json_files:
            with open(json_file,'r')as f:
                xen_funcs = json.load(f)

            for func_name,filename,linenumber,linenumberEnd in tqdm(xen_funcs):
                try:
                    func_code=read_func(os.path.join(project_root,filename[:-4],filename),linenumber,linenumberEnd)
                except Exception as e:
                    print("Error with",filename,e)
                    continue
                final.append({"filename": f'{func_name}_{index}.c', "code":func_code , "subcode" : "", "val" : 2})
                index+=1
    df = pandas.DataFrame(final)
    df.drop_duplicates(subset=["code"], keep='first', inplace=True)
    print("saving...",len(df))
    df.to_pickle('/home/ubuntu/issta2022/data/pkl/vulroberta/original_dataset/real_test/real_test3.pkl')
    # df.to_excel('/home/ubuntu/issta2022/data/pkl/vulroberta/original_dataset/real_test/real_test.xlsx')

def write_file(content,index):
    file_str=content
    filename=str(index)+'.c'
    save_dir='/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code/'+str(int(index/1e2))
    os.makedirs(save_dir,exist_ok=True)
    with open(os.path.join(save_dir,filename),'w') as f:
        f.write(file_str)


def extract_starcoder_dataset():

    # to load python for example
    ds = load_dataset("bigcode/starcoderdata", data_dir="c", split="train",cache_dir='/home/ubuntu/Pseudo-Labelling/starcoder_data/c')
    for i in tqdm(range(5980411)):
        write_file(ds[i]["content"],i)
    # print(len(ds))
import os
from tqdm import tqdm
import shutil
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor
import sys
from cpgqls_client import *
import time
import pexpect
# def multi_move(file):
#     dir = '/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code/'
#     index=int(int(file[:-2])/1e5)
#     dir2=os.path.join(dir,str(index))
#     # if not os.path.exists(dir2):
#     # os.makedirs(dir2,exist_ok=True)
#     shutil.move(os.path.join(dir,file), dir2)
# def move_files():
#     dir = '/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code/'
#     for i in range(82,85):
#         dir2=os.path.join(dir,str(i))
#         os.makedirs(dir2,exist_ok=True)
#     for file in tqdm(os.listdir(dir)):
#         if not file.endswith('.c'):
#             continue
#         multi_move(file)
        
#     print('Finished:',file)

def multi_move(param):
    file,i=param
    dir = f'/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code/{i}'
    dir1 = '/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code2/'
    index = int(int(file[:-2]) / 1e2) 
    dir2 = os.path.join(dir1, str(index))
    os.makedirs(dir2, exist_ok=True) 
    try:
        shutil.move(os.path.join(dir, file), dir2)
    except Exception as e:
        print(f"Failed to copy {file}: {e}")

def move_files(): 
    dir = '/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code/'
    # files = [f for f in os.listdir(dir) if f.endswith(".c")]
    # with ThreadPoolExecutor(max_workers=6) as pool:
    #      pool.map(multi_move, files)
    params=[]
    for i in range(8537):
        for file in os.listdir(os.path.join(dir,str(i))):
            params.append((file,i))
            # multi_move()
            # pbar.update(1)
    pbar=tqdm(params)
    with Pool(32)as p:
        ret=p.imap_unordered(multi_move, params)
        for r in ret:
            pbar.update(1)
         
def joern_parse(param):
    file, outdir=param
    os.system(f'sh /home/ubuntu/joern-cli/joern-parse {file} --nooverlays  --language c -o {outdir} ')   
def source2cpg():
    dir='/home/ubuntu/Pseudo-Labelling/starcoder_data/c/source_code'
    with open('/home/ubuntu/Pseudo-Labelling/json/processed.json','r')as f:
        process_set=json.load(f)
    process_set=set(process_set)
    params=[]
    print(len(os.listdir(dir)))
    for i in os.listdir(dir):
        bin_path=os.path.join('/home/ubuntu/joern-cli/workspace2/source_code',f'{i}_cpg.bin')
        if bin_path in process_set or os.path.exists(bin_path):
            continue
        params.append((os.path.join(dir,str(i)),os.path.join('/home/ubuntu/joern-cli/workspace2/source_code',f'{i}_cpg.bin')))
    pbar=tqdm(params)
    with Pool(8)as p:
        ret=p.imap_unordered(joern_parse,params)
        for r in ret:
            pbar.update(1)
            
def import_souce(client, file_path):
    # file_path为需要导入的bin文件路径
    # 该函数执行完之后，cpg被加载进joern server

    query = f'importCpg(\"{file_path}\",\"test\")'
    try:
        result = client.execute(query)
        if 'stderr' in result and result['stderr'].find('java') != -1:
            print('joern server error:'+result['stderr'])
            print(file_path)

            sys.exit(0)
        else:
            # print("import_souce progress: {}%: ".format(100), "▋" * 50)
            pass
    except Exception as e:
        print("-----import souce code failed!-----")
        print(file_path)
        sys.exit(0)

def importCpg(joern_fd,filepath,j):

    # time.sleep(5)
    query=f'importCpg(\"{filepath}\",\"test{j}\")'
    # query=f'importCpg(\"{filepath}\")'
    
    # joern_fd.expect("joern>")
    joern_fd.sendline(query)
    ret=joern_fd.expect("joern>",timeout=60)
    # output=joern_fd.before.decode()
    # print(output,ret)
 
        

def connect_server():
    # 和joern server连接，需提前运行./joern --server
    # 返回值为一个client对象，用于之后与joern server进行交互
    # 端口和用户名密码可修改，参照https://docs.joern.io/server
    # server_endpoint = "localhost:8080"
    # basic_auth_credentials = ("username", "password")
    # client = CPGQLSClient(server_endpoint, auth_credentials=basic_auth_credentials)
  

    child = pexpect.spawn("/home/ubuntu/joern-cli/joern -J-Xmx25G")
    ret=child.expect("joern>",timeout=60)
    # output=child.before.decode()
    # print(output)
    return child


def get_func_json(client,result_file):
    query='cpg.method.isNotStub.filter(node=>node.lineNumber!=node.lineNumberEnd).filterNot(_.name.contains(\"<\"))'\
    f'.map(node=>List(node.name,node.filename,node.lineNumber,node.lineNumberEnd)).toJson |> \"{result_file}\"'
    func_range=[]
    try:

        # client.expect("joern>")

        client.sendline(query)
        ret=client.expect("joern>",timeout=60)
        # # output=client.before.decode()
        # output=client.before.decode()
        # print(output)
        time.sleep(1)

        with open(result_file,'r')as f:
            func_range=json.load(f)
        # ret=os.system(f'rm {result_file}')
        # if ret!=0:
        #     print('rm file failed')
        

        return func_range
    except:
        print('wrong')
        return func_range

def source2json(j,process_num):
    json_dir=f"/home/ubuntu/Pseudo-Labelling/json/{j}"
    os.makedirs(json_dir,exist_ok=True)
    fd=connect_server()
    dir='/home/ubuntu/joern-cli/workspace2/source_code/'
    params=[]
    funcs_list=[]
    process_set=set()
    if os.path.exists(f'{json_dir}/final.json'):
        with open(f'{json_dir}/final.json','r')as f:
            funcs_list=json.load(f)
    if os.path.exists(f'{json_dir}/processed.json'):
        with open(f'{json_dir}/processed.json','r')as f:
            process_set=json.load(f)
        process_set=set(process_set)
    file_len=len(os.listdir(dir))
    for file in os.listdir(dir)[j*int(file_len/process_num):(j+1)*int(file_len/process_num)]:
        if os.path.join(dir,file) in process_set:
            continue
        if file.endswith('_cpg.bin'):
            params.append(os.path.join(dir,file))
    pbar=tqdm(total=len(params),desc=f'Processing {j}')

    # fd=importCpg()
    for i,file in enumerate(params):
        try:
            importCpg(fd,file,j)
            funcs_list+=get_func_json(fd,f'{json_dir}/{j}.json')
            # close_joern_process(proc)
            process_set.add(file)
            # if i and i%30==0:

            if i and i%100==0:
                with open(f'{json_dir}/final.json','w')as f:
                    json.dump(funcs_list,f)
                with open(f'{json_dir}/processed.json','w')as f:
                    json.dump(list(process_set),f)
                fd.close()
                fd=connect_server()
           
            pbar.update(1)
        except Exception as e:
            # print(e)
            print(f'Error in {file}')
            pbar.update(1)
            
            continue
        
    with open(f'{json_dir}/final.json','w')as f:
        json.dump(funcs_list,f,indent=2)
    with open(f'{json_dir}/processed.json','w')as f:
        json.dump(list(process_set),f,indent=2)
    fd.close()
        
    return j
# if __name__ == '__main__':
#     start=time.time()
#     # extract_starcoder_dataset()
#     extract_specific_project('starcoder')
#     # move_files()
#     source2cpg()
#     # process_num=8
#     # params=[i for i in range(process_num)]
#     # with Pool(8)as p:
#     #     ret=p.imap_unordered(partial(source2json,process_num=process_num),params)
#     #     for r in ret:
#     #         print(r)
#     source2json(0,6)
#     print(time.time()-start)
#
#
#     # cpg.method.isNotStub.filter(node=>node.lineNumber!=node.lineNumberEnd).filterNot(_.name.contains("<")).map(node=>List(node.name,node.filename,node.lineNumber,node.lineNumberEnd)).toJson |> "/home/ubuntu/Pseudo-Labelling/10000.json"