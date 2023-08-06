# Pencil Python Commons

## Publishing package to Pypi

```bash
python setup.py sdist bdist_wheel

pip install twine

twine upload dist/*
```