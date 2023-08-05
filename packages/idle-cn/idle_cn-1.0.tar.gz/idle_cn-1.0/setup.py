from os import path as os_path
from setuptools import setup

import idle_cn

this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]

setup(
    name='idle_cn',  # 包名
    python_requires='>=3.0.0', # python环境
    version=1.0,# 包的版本
    description="IDLE汉化管理器",  # 包简介，显示在PyPI上
    long_description=read_file('README.md'), # 读取的Readme文档内容
    long_description_content_type="text/markdown",  # 指定包文档格式为markdown
    url='https://github.com/YHL12345656/idle_cn',
    # 指定包信息，还可以用find_packages()函数
    packages=[
        'idle_cn'
    ],
    include_package_data=False,
)