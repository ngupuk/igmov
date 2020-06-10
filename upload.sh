# !/bin/sh

python setup.py sdist
twine upload dist/*
rm -rf dist igmov.egg-info