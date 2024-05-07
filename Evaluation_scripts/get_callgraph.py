import clang.cindex

# 设置libclang库的路径
clang.cindex.Config.set_library_file('D:\\leak\\cpp\\LLVM\\bin\\libclang.dll')

def get_call_graph(filename):
    index = clang.cindex.Index.create()
    try:
        tu = index.parse(filename)
    except clang.cindex.TranslationUnitLoadError as e:
        print("Error parsing translation unit:", e)
        for diag in e.diagnostics:
            print("Diagnostic:", diag.spelling)
        return None

    # 创建一个字典来存储函数调用图
    call_graph = {}

    # 辅助函数来获取函数调用
    def travel(node,funclist):
        if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            funclist.append(node.spelling)
        for child in node.get_children():
            travel(child,funclist)
        return funclist
    def findcg(root):
        for node in root.get_children():
            if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
                caller=node.spelling
                #print(caller)
                callee=travel(node,[])
                callee=set(callee)
                if callee:
                    call_graph[caller]=set(callee)

    # 遍历AST来获取函数调用信息
    findcg(tu.cursor)

    return call_graph

# 示例用法
if __name__ == "__main__":
    filename = "D:\\test\\test3.cpp"
    call_graph = get_call_graph(filename)
    if call_graph is not None:
        print(call_graph)
