import json
from turing_machine import *


CONFIG = None


if __name__ == "__main__":
    
    # reading the config file and setting the machine
    json_config_file = open('config/binary_palindrome.json')
    CONFIG = json.load(json_config_file)
    json_config_file.close()

    turing_machine = TuringMachine(CONFIG)
    print(turing_machine)

    string = input('\nMachine Input: ')
    if Validator.validate_input(CONFIG['alphabets'], string):
        turing_machine.process_input(string)
    else:
        print("Invalid input string!")



# test case for palindrome json:
# 1001001001     => accept
# 1010100010101  => accept
# 101001000101   => reject


# test case for divisiblity by 3 json:
# 10010 (binary) => accept
# 100010010      => accept
# 1011101        => reject
# 0101001        => reject