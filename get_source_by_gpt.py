import openai
import extract_func
import time
import requests
import tiktoken
openai.api_key = "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"




#openai.api_base="https://api.chatanywhere.cn"
def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens






# 调用 GPT-3 API
def generate_response(list):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=list,
        # max_tokens=400,
        temperature=0,
        n=1,
        stop=None
    )
    #return response.choices[0].text.strip()
    return response


def creat_message(filepath, startnum, endnum):
    func_text = extract_func.read_func(filepath, startnum, endnum)
    prompt="You are a C/C++ code auditor with extensive knowledge in vulnerability discovery, familiar with the code characteristics of various CWE and CVE vulnerabilities. Given a piece of ##code##, you will identify the TOP 5 lines of code that meet any of the following ##characteristics description##.Please omit the thought process and explanation, and directly provide the result list in json format {{\"result\" : [{{\"function_name\": function name,  \"statements\": statements,  \"variable\": target variable, \"line_number\" : line of statements}}]}} .\
##characteristics description##>>\
1. Uninitialized Pointer: Accessing an uninitialized pointer can lead to a null pointer reference.\
2. Null Pointer Dereference: Dereferencing a pointer in the code without checking if it is NULL.\
3. Memory Allocation Failure: When a memory allocation operation (such as malloc or new) fails and returns a NULL pointer, not checking this pointer can lead to a null pointer reference.\
4. Uninitialized or Incorrectly Assigned Pointer Variable: If a pointer variable is not correctly initialized or is mistakenly assigned NULL, it can lead to subsequent null pointer references.\
5. Returning a Null Pointer from a Function: If a function returns an uninitialized or NULL pointer, and its validity is not checked, it can lead to a null pointer reference.\
6. Array Out of Bounds: Accessing array elements when an array is out of bounds may cause the pointer to become NULL, thus leading to a null pointer reference.\
7. Improper Lifecycle Management of a Pointer: If the memory pointed to by a pointer is released during the pointer's lifecycle and the pointer is still used afterward, it can lead to a null pointer reference.\
8. Pointer Value Modified Before Use: If a pointer's value is accidentally modified to NULL or an uninitialized value before its use, it can lead to a null pointer reference.\
9. Unsynchronized Pointer Access in a Multithreaded Environment: In a multithreaded environment, if the access to a pointer is not properly synchronized, it can lead to a null pointer reference.\
10. Pointer Alias Problem: In the code, if there are multiple pointers pointing to the same memory location, and one of these pointers is released or changed, the others may become null pointers.\
##code##\n"+func_text
    return prompt

if __name__ == '__main__':
    prompt=creat_message("D:\leak\智能漏洞检测\CWE-476\source\jasper_476\jasper_476\CVE-2021-3443\CVE-2021-3443_CWE-476_f94e7499a8b1471a4905c4f9c9e12e60_jp2_dec.c_OLD.c",99,491)
    list_msg=[]
    list_msg.append({"role": "user", "content": prompt})
    res=generate_response(list_msg)
    print(res['choices'][0]['message']['content'])



