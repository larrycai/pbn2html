#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import io
import sys
import pkgutil

from string import Template

language="Chinese"

def pbn2html(pbn_file):
    all = {
        "generated" : "2020-12-01"
    }
    template = pkgutil.get_data(__name__,'template.html')
    src = Template(template.decode('utf-8'))
    result = src.safe_substitute(all)
    output = os.path.splitext(pbn_file)[0]+'.html'
    with io.open(output, "w", encoding="utf-8") as text_file:
        print("write to file %s" % output)
        text_file.write(result)


def main():
    # print(sys.argv)
    if len(sys.argv) > 1:
        param = sys.argv[1:]
        if param[0].endswith(".pbn"):
            pbn2html(param[0])
        else:
            print("pbn2html.py <file.pbn>")
    else:
        print("pbn2html.py <file.pbn>")

if __name__ == '__main__':
    main()
