from setuptools import find_packages, setup

setup(
    name='flaskcom',
    packages=find_packages(),
    version='0.2.4',
    description='',
    author='Johannes Twiefel',
    licence='MIT',
    install_requires=[
        "Flask==1.0.2",
        "requests>=2.20.0",
        "Flask-Login==0.5.0",
    ]
)
