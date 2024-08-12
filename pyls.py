import os
from datetime import datetime
import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="pyls",
        description="Lists files and directories in the current directory.",
        epilog="This is a limited implementation of the ls command."
    )
    
    parser.add_argument(
        "dirname",
        help="The directory to list files from.",
        action="store",
        nargs="?",
        default="."
    )
    
    parser.add_argument(
        "-F",
        "--filetype",
        help="Append a character to the names indicating file type.",
        action="store_true"
    )
    
    parser.add_argument(
        "-l",
        "--long-format",
        help="Show detailed information including last modified date and size.",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    file_lines = get_info_from_directory(args.dirname)
    formatted_results = format_results(file_lines, args.long_format, args.filetype)
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

def format_results(results, long_format, filetype):
    assert isinstance(results, list), "This should be a list"
    assert isinstance(long_format, bool), "Input type Boolean"
    assert isinstance(filetype, bool), "Input type Boolean"

    output_lines = []
    for item in results:
        name = item["name"]
        if filetype:
            if item["type"] == 'd':
                name += "/"
            elif item["type"] == 'x':
                name += "*"

        if long_format:
            size = str(item["size"])
            modification_time = item["mod_time"].strftime("%Y-%m-%d %H:%M:%S")
            if item["type"] == 'd' and not filetype:
                name += "/"
            output_lines.append(f"{modification_time}\t{size}\t{name}")
        else:
            output_lines.append(name)

    return output_lines

def show_results(lines):
    assert isinstance(lines, list), "This should be a list"
    for line in lines:
        print(line)

if __name__ == '__main__':
    main()
