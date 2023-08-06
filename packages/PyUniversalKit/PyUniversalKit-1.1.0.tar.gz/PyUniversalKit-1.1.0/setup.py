import setuptools
from setuptools import find_packages

setuptools.setup(
    name = "PyUniversalKit",
    version = "1.1.0",
    author = "MatthewYt",
    author_email = "2158707744@qq.com",
    description = "Hello,PyUniversalKit!",
    packages = find_packages(),
    url='https://github.com/yangtang-special/PyUniversalKit',
    long_description_content_type = "text/markdown",
    data_files = ["README.md"],
    long_description = open('README.md',encoding="utf-8").read(),
    install_requires = [
        "requests",
        "prettytable",
        "lxml",
        "colorama"
    ]

)

