# Nitrokey DFU tool - nkdfu

`nkdfu` is a Python DFU tool for updating Nitrokeys' firmware. Currently supports Nitrokey Pro only.

Based on [python-dfu] project, which brings implementation of USB DFU 1.1 spec.

## Call

```
nkdfu FIRMWARE_PATH <flags>
```

See `nkdfu --help` for details.

## Installation
Package is not published yet, however it is possible to install it directly from the releases page:

```bash
pip3 install https://github.com/Nitrokey/nkdfu/releases/download/v0.1/nkdfu-0.1-py3-none-any.whl
```

## License
License follows upstream - GPLv2. See [LICENSE] for details.


[LICENSE]: ./LICENSE
[python-dfu]: https://github.com/vpelletier/python-dfu