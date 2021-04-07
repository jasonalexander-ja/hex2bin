import re
import os
import sys
import os.path

def get_command_args():
    if len(sys.argv) != 3:
        print("Please specify 2 arguments \"python hex-dump-conv.py input-file.txt output-file.bin\"")
        sys.exit()
    return (sys.argv[1], sys.argv[2])

def get_input_file(file_name):
    output = ""
    try:
        output = open(file_name, "r")
    except:
        print(f"Couldn't open file: {file_name}")
        sys.exit()
    return output

def get_output_file(file_name):
    if os.path.isfile(file_name):
        cont = input("The specified output file already exists, continue Y/N: ").capitalize()
        if cont.startswith("N"):
            sys.exit()
    try:
        return open(file_name, "wb")
    except:
        print(f"Couldn't create file at directory: {file_name}; please ensure this directory exists.")
        sys.exit()

def check_values(file):
    if len(file) % 2 != 0:
        print("File needs to be a multiple of 2, each hex code contains 2 characters")
        sys.exit()
    for pos, val in enumerate(file):
        if not re.search("[A-F]|[0-9]", val):
            print(f"Error at position: {pos}, value: {val}; Hex characters need to be 0-9 or A-F")
            sys.exit()

def format_file(file_in):
    file = file_in.upper()
    to_replace = [" ", "\n","\r","\t","\f","\v"]
    for val in to_replace:
        file = file.replace(val, "")
    return file 

def parse_input(file_in):
    file = format_file(file_in)
    check_values(file)
    output = []
    for pos in range(0, len(file), 2):
        value_str = f"0x{file[pos]}{file[pos + 1]}"
        output.append(int(value_str, 16))
    return bytearray(output)

def main():
    (input_name, output_name) = get_command_args()

    input_file = get_input_file(input_name)
    data = parse_input(input_file.read())

    output_file = get_output_file(output_name)
    output_file.write(data)
    
    input_file.close()
    output_file.close()

main()
