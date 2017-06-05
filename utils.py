#encoding: utf-8

import os

def write_log(file_name, content):
    DIR = "./content/"
    filePath = os.path.join(DIR, file_name)
    print filePath
    with open(filePath, "w") as f:
        f.write(content)
