from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(["ADOFAICore_cython_compile.py"], annotate=True))