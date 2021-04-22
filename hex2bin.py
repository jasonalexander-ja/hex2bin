import re
import os
import sys
import os.path
import binascii

# gets the Command line arguments, it will print the response if there are not 3 arguments.
def get_command_args():
    if len(sys.argv) != 4:
        print("Please specify 3 arguments \"python hex-dump-conv.py input-file.txt output-file.bin data_type (hex/bin)\"")
        sys.exit()
    return (sys.argv[1], sys.argv[2], sys.argv[3])

# Gets this file name, depending on the datatype being read it will either read it bytes or string
def get_input_file(file_name, data_type):
    output = ""
    try:
        if data_type.lower() == "bin":
            output = open(file_name, "r")
        elif data_type.lower() == "hex":
            output = open(file_name, "rb")
    except:
        print(f"Couldn't open file: {file_name}")
        sys.exit()
    return output

# Creates new file in the specified directory, depending on the data_type.
def get_output_file(file_name, data_type):
    if os.path.isfile(file_name):
        cont = input("The specified output file already exists, continue Y/N: ").capitalize()
        if cont.startswith("N"):
            sys.exit()
    try:
        if data_type.lower() == "bin":
            return open(file_name, "wb")
        elif data_type.lower() == "hex":
            return open(file_name, "w")
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
# converts the file to binary and will convert the contents accordingly
def parse_input(file_in):
    file = format_file(file_in)
    check_values(file)
    output = []
    for pos in range(0, len(file), 2):
        value_str = f"0x{file[pos]}{file[pos + 1]}"
        output.append(int(value_str, 16))
    return bytearray(output)

def hex_convert(data_in):
    try:
        conv = binascii.hexlify(data_in)
    except:
        print("Unable to convert the binary file to a hex file")
        sys.exit()
    return conv

def main():
    try:
        (input_name, output_name, data_type) = get_command_args()
    except:
        print("please type: python hex2bin.py filelocation output location datatype /n use Bin to convert the file to a binary file, use hex to convert the file to a hexadecimal file.")

    input_file = get_input_file(input_name, data_type)

    if data_type.lower() == "bin":
        data = parse_input(input_file.read())

        output_file = get_output_file(output_name, data_type)
        output_file.write(data)
    elif data_type.lower() == "hex":
        hexdata = hex_convert(input_file.read())

        output_file = get_output_file(output_name+".txt", data_type)
        output_file.write(str(hexdata))
    else:
        print("Invalid parameters")
        sys.exit()

    input_file.close()
    output_file.close()

main()
