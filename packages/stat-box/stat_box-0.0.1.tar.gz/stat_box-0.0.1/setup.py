from setuptools import setup, find_packages
from os.path import join, dirname

try:
    with open(join(dirname(__file__), 'readme.md')) as fh:
        long_description = fh.read()
except:
    long_description = 'Convinient statistical description of dataframes.'

setup(
    name="stat_box",
    packages=find_packages(),
    version="0.0.1",
    license="GPLv3",
    description="Convinient statistical description of dataframes.",
    author="dmatryus",
    author_email="dmatryus.sqrt49@yandex.ru",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.com/dmatryus.sqrt49/stat_box",
    keywords=["STATICS"],
    install_requires=["scipy"],
)
