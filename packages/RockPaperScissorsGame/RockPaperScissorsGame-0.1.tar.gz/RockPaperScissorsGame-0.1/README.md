# Uploading package to the Python Package Index (PyPi)

You may want to set up a virtual environment before running the commands listed below (run ~/github/rock-paper-scissors/build_tools/build_source.sh).

```python
cd ~/github/rock-paper-scissors/package
python setup.py sdist

pip install twine
# commands to upload to pypi test repository
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install --index-url https://test.pypi.org/simple/ RockPaperScissorsGame

# commands to upload to pypi repository
twine upload dist/*
pip install rockpaperscissors
```

### Note

Running `python setup.py sdist` will create a `dist` folder and a `RockPaperScissorsGame.egg-info` folder.  These can be deleted after the package is uploaded to pypi and do not need to be uploaded to the github repository.  They also need to be deleted and regenerated if any changes are made to the package source files.