from setuptools import setup

setup(
    name='igmov',
    version='1.0.0',
    description='Video generator using Ngupuk templates',
    license='MIT',
    packages=['igmov'],
    author='Ngupuk',
    author_email='wafax.4@gmail.com',
    url='https://github.com/ngupuk/igmov',
    install_requires = [
        'moviepy', 'urllib3'
    ]
)