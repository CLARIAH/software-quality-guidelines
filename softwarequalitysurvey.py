#!/usr/bin/env python3

from __future__ import print_function, unicode_literals, division, absolute_import #python 2 compatibility

import io #python 2 compatibility
import os
import sys
import argparse
from collections import OrderedDict

def latextomarkdown(s):
    return s.replace('\\&','&')

responseoptions = OrderedDict((('NA', 'Not applicable'), (0,'No'), (1,'Minimal'), (2,'Adequate'), (3,'Good'), (4,'Perfect')))

def getresponse():
    print("    Response options: " ,file=sys.stderr)
    for code, label in responseoptions.items():
        print("      " + str(code) +') ' + label, file=sys.stderr)
    first = True
    response = None
    while response not in ( str(key) for key in responseoptions):
        if not first:
            print("(Invalid response)",file=sys.stderr)
        if sys.version[0] == '2':
            response = raw_input("Your response> ")
        else:
            response = input("Your response> ")
    if response == 'NA':
        return None
    else:
        return int(response)

def getcomments():
    prompt = "Optional comments (just press ENTER to discard)> "
    if sys.version[0] == '2':
        comments = raw_input(prompt)
    else:
        comments = input(prompt)
    return comments

def main():
    parser = argparse.ArgumentParser(description="Software Quality Survey", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--template','-t', help="Output a template, do not survey interactively", action='store_true',default="",required=False)
    args = parser.parse_args()

    #args.storeconst, args.dataset, args.num, args.bar
    texfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'softwareguidelines.tex')
    buffer = []

    criteria = OrderedDict()
    category = None

    begincriteria = False
    with io.open(texfile,'r',encoding='utf-8') as f:
        for line in f:
            if line.startswith('%BEGINCRITERIA'):
                begincriteria = True
            elif line.startswith('%ENDCRITERIA'):
                begincriteria = False
            elif line.startswith('\\subsection') and begincriteria:
                category = latextomarkdown(line[12:line.find('}')])
                criteria[category] = OrderedDict()
            elif line.startswith('\\indicator'):
                code = buffer[-3][buffer[-3].rfind('{')+1:-1]
                label = buffer[-1][buffer[-1].rfind('{')+1:-1]
                criteria[category][code] = latextomarkdown(label)
            else:
                buffer.append(line.strip())


    print("CLARIAH Software Quality Survey")
    print('=====================================================================')
    print()
    print()


    responses = {}
    for category, categorydata in criteria.items():
        print(category)
        print('---------------------------------------------------------------------')
        for code, label in categorydata.items():
            print('* **' + code + '**: ' + label)
            if args.template:
                print('    * Response: ``Not Applicable / No / Minimal / Adequate / Good / Perfect``')
                print('    * Comments:')
            else:
                response = getresponse()
                if response is not None:
                    responses[code] = response
                print('    * Response: ``' + responseoptions[response] + '``')
                comments = getcomments().strip()
                if comments:
                    print('    * Comments: ' + comments)
                print(file=sys.stderr)

        print()
        print()



if __name__ == '__main__':
    main()
