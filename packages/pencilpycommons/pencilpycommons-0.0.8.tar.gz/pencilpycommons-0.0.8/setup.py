from setuptools import setup, find_packages

setup(
    name='pencilpycommons',
    version='0.0.8',
    packages=find_packages(exclude=("tests",)),
    license='MIT',
    description='Commons library',
    long_description='Commons library',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=
    [
        "boto3==1.11.8",
        "redis==3.5.3",
        "peewee==3.13.1",
        "PyMySQL==0.9.3",
        "pika==0.13.1",
        "requests==2.26.0"
    ],
    author='Abhinav',
    author_email='abhinav@trypencil.com'
)
