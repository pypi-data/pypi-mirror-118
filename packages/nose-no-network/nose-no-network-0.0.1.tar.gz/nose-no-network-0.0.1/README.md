Simplest possible [nose](https://nose.readthedocs.io/en/latest/) plugin to
disable network access during tests. 

## Installation

```console
pip install nose-no-network
```

## Usage

```console
nosetests --with-no-network ...
```

## How it works

nose-no-tests works by monkey patching `socket.socket` to throw an exception.

## License

nose-no-network is licensed under the MIT license.

## Authors

* [Ross McFarland](https://github.com/ross)
