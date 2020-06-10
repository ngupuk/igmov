from setuptools import setup
import os.path
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

setup(
    name='igmov',
    version='0.0.0-alpha',
    description='Video generator using Ngupuk templates',
    long_description= read_file('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=['igmov'],
    author='Ngupuk',
    author_email='wafax.4@gmail.com',
    url='https://github.com/ngupuk/igmov',
    install_requires = [
        'moviepy', 'urllib3'
    ]
)