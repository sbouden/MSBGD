'''Extracts mails addresses
usage: extractor.py input.txt output.txt

Every line of output.txt contains a single mail address.
Note: the formatting of the output is already taken care of
by our template, you just have to complete the function
extractMail below.

(Public skeleton code)'''

import sys
import re

if len(sys.argv) != 3:
    print(__doc__)
    sys.exit(-1)

def extractMail(content):
    # Code goes here
    # this function should return a list of string
    # emails = re.findall(r"\s+[\sa-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", content)
    emails = re.findall(r"[\w\.=+-]+[\w\.=+-]+@[\w\.=+-]+\.[\w\.=+-]+", content)
    return emails

inputContent = ""
with open(sys.argv[1], 'r', encoding="utf-8") as input:
    inputContent = input.read()
    
with open(sys.argv[2], 'w', encoding="utf-8") as output:
    for mail in extractMail(inputContent):
        output.write(mail + "\n")

