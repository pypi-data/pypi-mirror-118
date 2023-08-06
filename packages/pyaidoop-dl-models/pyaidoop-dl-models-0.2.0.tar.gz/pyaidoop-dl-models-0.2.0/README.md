# pyaidoop-dl-models
aidoop-dl-models python package module

## Prerquisites
### install object detection api module
```bash
# clone tensorflow models
git clone https://github.com/tensorflow/models.git

# install protobuf if protobuf not installed
apt install protobuf-compiler

# setup models
cd models/research
# compile protos:
protoc object_detection/protos/*.proto --python_out=.
# Install TensorFlow Object Detection API as a python package:
cp object_detection/packages/tf2/setup.py .
python -m pip install .
```

## Setup
### setup commands
```
pip install -r requirements.txt
pip install --upgrade pip
pip install twine
python setup.py install
python setup.py sdist bdist_wheel
python -m twine upload dist/*
```