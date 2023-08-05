# packaging_tutorial
View at: [https://test.pypi.org/project/example-pkg-bigabig/0.0.1/](https://test.pypi.org/project/example-pkg-bigabig/0.0.1/)

## Create TestPyPi Account
[https://test.pypi.org/account/login/](https://test.pypi.org/account/login/?next=%2Fmanage%2Faccount%2F#api-tokens)

## Commands

### Setup
```
conda create -n tutorial python=3.8
conda activate tutorial
python3 -m pip install --upgrade pip
```

### Build
```
python3 -m pip install --upgrade build
python3 -m build
```

### Upload
```
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

### Install
```
python3 -m pip install --index-url https://test.pypi.org/simple/ example-pkg-bigabig
```

