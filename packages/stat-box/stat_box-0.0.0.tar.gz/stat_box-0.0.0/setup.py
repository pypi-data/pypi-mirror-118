from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="stat_box",
    packages=find_packages(),
    version="0.0.0",
    description="Convinient statistical description of dataframes.",
    author="dmatryus.sqrt49@yandex.ru",
    long_description="A project for convinient statistical description of dataframes. See readme for more details.", #long_description,
    install_requires=["scipy"],
)
