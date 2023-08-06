from setuptools import setup, find_packages 
import codecs
import os 

def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), "r",encoding='utf-8').read()


def get_version():
    '''
    version_file = 'pipetools/version.py'
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']
    '''
    return '0.0.1'

setup(
    name='pipecv',
    version=get_version(),
    description="主要用于通用，无依赖的工具集，如文本、转换的读取、基础的IO",
    author='zhys513',#作者
    author_email="254851907@qq.com",
    url="https://gitee.com/zhys513/pipetools",
    python_requires='>=3.6', 
)

