import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser(
    prog="pyls",
    description="this command lists all the files in the selected directory",
    epilog="this is my ls",
)

parser.add_argument(
    "dirname",
    help="this command outputs the name of the directory",
    action="store",
    nargs="?",
    default=".",
)

parser.add_argument(
    "-F",
    "--filetype",
    help="this shows the filetype of the file e.g .exe, .jpg, .py",
    action="store_true",
)

parser.add_argument(
    "-l",
    "--long-format",
    help="this provides extra information about the file. like the name, date it was created/modiefied and other things",
    action="store_true",
)

args = parser.parse_args()

def main(args):
    file_lines = get_info_from_directory(args.dirname)
    formatted_results = formatResults(file_lines, args.long_format, args.filetype)
    show_results(formatted_results)


def get_info_from_directory(directory_name):
 
    assert os.path.isdir(directory_name), "directory_name should be an existing directory"

    file_descriptions = []

    for item in os.listdir(directory_name):
        full_path = os.path.join(directory_name, item)

        if os.path.isdir(full_path):
            type_of_file = "d"  
            size_of_file = 0  
        elif os.path.isfile(full_path):
            type_of_file = "f"  
            size_of_file = os.path.getsize(full_path)  
        else:
            continue 

        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            type_of_file = "x"
            
        modification_time = datetime.fromtimestamp(os.path.getmtime(full_path)).replace(microsecond=0)

        file_descriptions.append({
            "mod_time": modification_time,
            "size": size_of_file,
            "type": type_of_file,
            "name": item
        })

    return file_descriptions

def formatResults(results, long_format, filetype):
    """
    Processes a list of file details and display options
    to generate a list of formatted strings for output.

    Parameters:
    results = A list of dictionaries, similar to the output of get_info_from_directory()
    long_format = A boolean flag to specify if the output should include detailed information.
    filetype = A boolean flag to determine if an extra type indicator should be appended.

    Returns:
    A list of formatted strings.
    """
    assert isinstance(results, list), "This should be a list"
    assert isinstance(long_format, bool), "Input type Boolean"
    assert isinstance(filetype, bool), "Input type Boolean"

    output_lines = []

    for item in results:
        size = str(item.get("size", 0))
        modification_time = str(item.get("mod_time", ""))
        name = item.get("name", "")
        filetype_char = item.get("type", "")
        
        if long_format:
            if filetype:
                if filetype_char == 'd':
                    name += "/"
                elif filetype_char == 'x':
                    name += "*"
                output_lines.append(f"{modification_time}\t{size}\t{name}")
            else:
                if filetype_char == 'd':
                    name += "/"
                output_lines.append(f"{modification_time}\t{size}\t{name}")
        
        elif filetype:
            if filetype_char == 'd':
                name += "/"
            elif filetype_char == 'x':
                name += "*"
            output_lines.append(name)
        
        else:
            if filetype_char == 'd':
                name += "/"
            output_lines.append(name)

    return output_lines