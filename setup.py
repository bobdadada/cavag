from setuptools import setup, find_packages

setup()

import os

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
    os.rmdir(path)

dirs = ['dist','fcre.egg-info','build']
for dir_ in dirs:
    if not os.path.isdir(dir_):
        continue
    del_file(dir_)
