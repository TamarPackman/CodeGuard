import ast
import io
import zipfile
from services.UnusedVariableTracker import ScopeTracker
async  def  extract_python_files (file) :
    content = await file.read()
    zip_bytes = io.BytesIO(content)
    python_files = {}
    with zipfile.ZipFile(zip_bytes) as zip_file:
        for f in zip_file.namelist():
            if f.endswith(".py"):
                try:
                 with zip_file.open(f) as file_handle:
                    python_files[f] = file_handle.read().decode("utf-8")
                except Exception as e:
                 raise ValueError(f"Error reading contents of file {f}: {e}") from e
    return python_files




def get_count_missing_docstrings(tree,missing_docstrings=None):#פונקציה שבודקת כמה פונקציות אין להן תיעוד
    count=0
    for node in ast.walk(tree):
        if isinstance(node,ast.FunctionDef) or isinstance(node,ast.AsyncFunctionDef):
            if ast.get_docstring(node)==None:
                count+=1
                if missing_docstrings != None:
                    if node.name in missing_docstrings:
                        missing_docstrings[node.name].append({"line":node.lineno})
                    else:
                        missing_docstrings[node.name]=[{"line":node.lineno}]
    return count
def get_length_function(tree,function_lengths):

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or  isinstance(node,ast.AsyncFunctionDef):
                length = node.end_lineno - node.lineno + 1
                function_lengths[node.name]=length
    return function_lengths



def get_count_unused_variables(tree,unused_variables=None):
    tracker = ScopeTracker()
    tracker.visit(tree)
    if unused_variables !=None:
     unused_variables.update(tracker.defined_vars)
    return sum(
    1 for uses in tracker.defined_vars.values()
    for entry in uses
    if entry["use"] is False
)