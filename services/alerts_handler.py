import ast
import services.common_analysis as common_analysis

def get_alerts_data(py_file,source_code,result):
    function_length={}
    File_Length={}
    unused_variables={}
    Missing_Docstrings={}
    lines = source_code.splitlines()
    num_lines = len(lines)
    if num_lines>=200:
        File_Length["line"]=num_lines
    tree = ast.parse(source_code)
    function_length=common_analysis.get_length_function(tree,function_length)
    function_length = {key: value for key, value in function_length.items() if value >= 20}
    common_analysis.get_count_unused_variables(tree,unused_variables)
    unused_variables = {
        key: [{"in": item["in"]} for item in items if not item.get('use', True)]
        for key, items in unused_variables.items()
        if any(not item.get('use', True) for item in items)
    }
    common_analysis.get_count_missing_docstrings(tree,Missing_Docstrings)
    result[py_file]={
        "Function Length": function_length,
        "File Length": File_Length,
        "Unused Variables": unused_variables,
        "Missing Docstrings": Missing_Docstrings
    }