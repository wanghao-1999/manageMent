from setuptools import setup, find_packages

setup(
    name='document_management',
    version='1.0.0',
    description='A document management system',
    author='ZouLongFei',
    author_email='zoulongfei@jxclkj.com',
    packages=find_packages(),
    install_requires=[
        'asgiref==3.7.2'
        'Django==4.2.4'
        'sqlparse==0.4.4'
        'typing_extensions==4.7.1'
        'tzdata==2023.3'

    ],
)
