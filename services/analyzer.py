import ast
import os
import services.common_analysis as common_analysis
def get_analysis_data(py_files):
    function_lengths={}
    issue_counts_by_type = {
        "Function Length": 0,
        "File Length": 0,
        "Unused Variables": 0,
        "Missing Docstrings": 0
    }
    problems_by_file={}
    for py_file,source_code in py_files.items():
        count_problems=0
        lines = source_code.splitlines()
        num_lines = len(lines)
        issue_counts_by_type["File Length"] +=1 if num_lines > 200 else 0
        tree = ast.parse(source_code)
        length_function_for_single_file={}
        length_function_for_single_file=common_analysis.get_length_function(tree,length_function_for_single_file)
        length_function_for_single_file = {key + f"_{py_file }": value for key, value in length_function_for_single_file.items()}
        function_lengths=function_lengths|length_function_for_single_file
        count_issues_by_type(tree, issue_counts_by_type,function_lengths)

        count_problems=get_count_function_length_problem(tree,length_function_for_single_file)+common_analysis.get_count_unused_variables(tree)+common_analysis.get_count_missing_docstrings(tree)+(1 if num_lines > 200 else 0)
        problems_by_file[py_file] =count_problems

    return {
        "function_lengths": function_lengths,
        "issue_counts_by_type": issue_counts_by_type,
        "detailed_file_issues": problems_by_file
    }


#func that get all the problems and count issues by type
def count_issues_by_type(tree,issue_counts_by_type,function_lengths):
    count_function_length= get_count_function_length_problem(tree,function_lengths)
    issue_counts_by_type["Function Length"]+=count_function_length
    count_unused_variables=common_analysis.get_count_unused_variables(tree)
    issue_counts_by_type["Unused Variables"]+=count_unused_variables
    issue_counts_by_type["Missing Docstrings"]+=common_analysis.get_count_missing_docstrings(tree)
def get_count_function_length_problem(tree,length_function):
    count = sum(1 for length in length_function.values() if length > 20)
    return count;