from setuptools import setup
import os.path
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
    packages=['igmov'],
    install_requires = [
        'moviepy', 'urllib3'
    ]
)