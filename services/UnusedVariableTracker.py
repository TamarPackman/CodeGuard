import ast
import builtins
class ScopeTracker(ast.NodeVisitor):
    def __init__(self):
        self.start =[]
        self.func_name=[]
        self.func_name.append("global")
        self.start.append(0)

        self.end = []
        self.end.append(float('inf'))
        self.defined_vars = {}
    def new_scope(self,start,end,node):
        self.start.append(start)
        self.end.append(end)
        self.func_name.append(node.name)
    def finish_scope(self):
        self.start.pop()
        self.end.pop()
        self.func_name.pop()
    def contains(self,list_of_v):
        for v in list_of_v:
            if v["start"]<=self.start[-1] and v["end"]>=self.end[-1]:
                return v
        return  None

    def visit_FunctionDef(self, node):
        self.new_scope(node.lineno, node.end_lineno,node)
        self.var_in_func(node)
        self.generic_visit(node)
        self.finish_scope()
    def var_in_func(self,node):
        param_names = [arg.arg for arg in node.args.args + node.args.kwonlyargs]
        if node.args.vararg:
            param_names.append(node.args.vararg.arg)
        if node.args.kwarg:
            param_names.append(node.args.kwarg.arg)
        for var_name in param_names:
            if var_name in self.defined_vars:
                self.defined_vars[var_name].append({
                    "start": self.start[-1],
                    "end": self.end[-1],
                    "in":self.func_name[-1],
                    "use": False
                })
            else:
                self.defined_vars[var_name] = [{
                    "start": self.start[-1],
                    "end": self.end[-1],
                    "in":self.func_name[-1],
                    "use": False
                }]
    def visit_ClassDef(self, node):
        self.new_scope(node.lineno, node.end_lineno,node)
        self.generic_visit(node)
        self.finish_scope()

    def visit_AsyncFunctionDef(self, node):
        self.new_scope(node.lineno, node.end_lineno,node)
        self.var_in_func(node)
        self.generic_visit(node)
        self.finish_scope()

    def visit_Name(self, node):
        if node.id in dir(builtins):
            return
        if isinstance(node.ctx, ast.Store):
            if node.id in self.defined_vars:
                 if self.contains(self.defined_vars[node.id])==None:
                     self.defined_vars[node.id].append({"start": self.start[-1],
                                       "end": self.end[-1],
                                        "in":self.func_name[-1],
                                       "use": False})
            else:
             self.defined_vars[node.id]=[{"start":self.start[-1],"end":self.end[-1],"in":self.func_name[-1],"use":False}]

        elif isinstance(node.ctx,ast.Load):

            if node.id  in self.defined_vars:
                v=self.contains(self.defined_vars[node.id])
                if v!=None:
                    v["use"]=True
        self.generic_visit(node)

