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
