# 转换.py文件为.pyd文件，需要安装Cython

import sys, os
from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

# scan directory
def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if path.endswith('__init__.py'):
            continue
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(path.replace(os.path.sep, ".")[:-3])
        elif os.path.isdir(path):
            scandir(path, files)
    return files
    
# generate an Extension object from its dotted name
def makeExtension(extName):
    extPath = extName.replace('.', os.path.sep) + '.py'
    ext = Extension(
        extName,
        [extPath],
    )
    return ext
    
extNames = scandir('fcre')
extensions = [makeExtension(name) for name in extNames]

# delete all *.py file except */__init__.py
def deletePy(dir):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if path.endswith('__init__.py'):
            continue
        if path.endswith('.py'):
            os.remove(path)
        elif os.path.isdir(path):
            deletePy(path)

setup(
  name = 'cavag'',
  packages = ['cavag'],
  ext_modules = cythonize(extensions, compiler_directives={'language_level': 3}),
)

