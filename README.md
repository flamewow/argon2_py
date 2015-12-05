Python bindings for argon2 : https://github.com/P-H-C/phc-winner-argon2

Installation:
You can install argon2_py from this repository if you want the latest but possibly non-compiling version:

$ git clone --recursive https://github.com/flamewow/argon2_py
$ cd argon2_py
$ python setup.py build

Become superuser (or use virtualenv):
# python setup.py install

Or you can install the latest release from PyPi:
$ pip install argon2

Example:
    >>> import argon2
    >>> argon2.argon2_hash("password","some_salt")
    b'\xa8&x\xc7\xd9\xc4\x1f\xdf[2\xd9hq\xab\xe5\xb4WV\x89\xca\xa4\xee\xb3\x98\xf1I\xd1\xdaf\xe7=\xfaA\x04\xeb\xe1\xfd\x94)\xad\x84\r\x9ed<8xE\xc3\xd3\xfb\x13\xcbN\xcf\\}\xfd-9\x8b\x07@\xd8\x10\x1a\x83\x05\xd5\xfd\xc4m\x9f\xd7\x81\xdcX\x87\xb2\x02\xa9R\xc1\x9d\xaf6\xbb\x8c\xe1vH+\x07\xc7Y\x80\xb3\xb5\xf8\xba\xbd\x87\xd8\xf5\xea\x1a\x04V&\xf7\xde\x9b\x93\x8dbQ\x91e\xf6\xd6\xa2\xd8G8\xe3\x9a\x03\xf3'

