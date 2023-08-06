# Appyx
Note: [this is a good reference for updating Appyx version](https://widdowquinn.github.io/coding/update-pypi-package/)
## Preparation
Ensure you have local packages for distribution. Run these commands in your virtualenv:

```
python -m pip install --upgrade setuptools wheel
python -m pip install --upgrade twine
```

## To upload an Appyx version to PyPi
First, change the version number in file setup.py

To generate the distribution:
```
python3 setup.py sdist bdist_wheel
```

To upload:
```
python3 -m twine upload dist/*
```