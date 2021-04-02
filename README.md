
# hex2bin

Converts text files containing valid hexadcimal bytes into binary-format files.

### Example
`python hex2bin.py path-to-input.txt path-to-output.bin`
### Errors
The input files requires there to be an even number of characters, as a byte is always 2 hex characters. All the characters are required to be either between 0-9 or A-F/a-f, all letters are case insensitive. 

Any whitespace/tabs/returns/new lines/form feed and vertical tabs will be ignored. 
