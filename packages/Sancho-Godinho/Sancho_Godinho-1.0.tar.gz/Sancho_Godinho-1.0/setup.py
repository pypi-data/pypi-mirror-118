from setuptools import setup, find_packages
import os

setup_args=dict(
    name="Sancho_Godinho",
    version="1.0",
    author="Sancho Godinho",
    description="A Simple About Me Page in Python",
    long_description='This is A Simple About Sancho Godinho Page.',
    packages=['Sancho_Godinho'],
    keywords=[],
    url="https://code.sololearn.com/c3199qcbgCVa/?ref=app",
    license_files = ('LICENSE.txt'),
    project_urls={
        "Bug Tracker": "https://code.sololearn.com/c3199qcbgCVa/?ref=app",
        }
    )
install_requires=[]

if __name__=='__main__':
    setup(**setup_args, install_requires=install_requires)
