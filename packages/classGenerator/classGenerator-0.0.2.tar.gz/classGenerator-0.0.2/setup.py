from setuptools import setup, find_packages

readme = open("./README.md", "r")

setup(
    name='classGenerator',
    version='0.0.2',
    license='MIT',
    packages=find_packages(),
    description='Generador de clases en python',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Daniel Dubon Rodriguez',
    author_email='danieldubon499@gmail.com',
    url='https://github.com/DanielDubonDR/CreateClasses.git',
    keywords=['class','object','createClass','generateClass','generatorClass'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
