import os
from datetime import datetime
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="pyls",
        description="this command lists all the files in the selected directory",
        epilog="This is a simple implementation of the `ls` command."
    )

    parser.add_argument(
        "dirname",
        help="Directory to list files from",
        nargs="?",
        default=".",
    )

    parser.add_argument(
        "-F",
        "--filetype",
        help="Append character indicating file type (e.g., / for directories, * for executables)",
        action="store_true",
    )

    parser.add_argument(
        "-l",
        "--long-format",
        help="Show detailed information: modification date, size, and name",
        action="store_true",
    )

    return parser.parse_args()

def main():
    args = parse_arguments()
    file_lines = get_info_from_directory(args.dirname)
    formatted_results = format_results(file_lines, args.long_format, args.filetype)
    show_results(formatted_results)

def get_info_from_directory(directory_name):
    if not os.path.isdir(directory_name):
        raise NotADirectoryError(f"{directory_name} is not a valid directory")

    file_descriptions = []
    for item in os.listdir(directory_name):
        full_path = os.path.join(directory_name, item)

        if os.path.isdir(full_path):
            type_of_file = "d"
            size_of_file = 0
        elif os.path.isfile(full_path):
            type_of_file = "f"
            size_of_file = os.path.getsize(full_path)
            if os.access(full_path, os.X_OK):
                type_of_file = "x"
        else:
            continue

        modification_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M:%S")

        file_descriptions.append({
            "mod_time": modification_time,
            "size": size_of_file,
            "type": type_of_file,
            "name": item
        })

    return file_descriptions

def format_results(results, long_format, filetype):
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
            modification_time = item["mod_time"]
            output_lines.append(f"{modification_time}\t{size}\t{name}")
        else:
            output_lines.append(name)

    return output_lines

def show_results(lines):
    for line in lines:
        print(line)

if __name__ == '__main__':
    main()
