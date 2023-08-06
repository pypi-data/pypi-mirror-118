from setuptools import setup
import setuptools
import pathlib



HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md" ).read_text()
setup(
    name ='viperthon',
    version ='0.0.1',
    desription ='Tool to perform basic operation on your Dataset',
    author='Swati Pandey',
    #url = '',
    long_description =README,
    long_description_content_type = 'text/markdown',
    packages = setuptools.find_packages(),
    license = "MIT",
    keyword =['read csv', 'basic operations on dataset','read categorical column'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],

    python_requires = '>=3.6',
    py_module = ['viperthon'],
    package_dir = {"":"src"},
    install_requires = ['pandas']



)