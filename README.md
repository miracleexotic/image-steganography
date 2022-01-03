# Image Steganography

**Note**: Simple image steganography make by python3

### Install
git clone
```console
$ git clone https://github.com/miracleexotic/image-steganography.git
```

with **setuptools**
```console
$ pip install --editable .
```

with **python pip**
```console
$ pip install -r requirements.txt
```

### Used
with **setuptools**
```console
$ steganography
Usage: steganography [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  decode
  encode
```

with **python3**
```console
$ python Steganography.py
Usage: steganography [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  decode
  encode
```
##### Quickstart
![Image Steganography encode with secrete message](/assets/images/encode_t1.png "Encode")
![Image Steganography decode](/assets/images/decode_t1.png "Decode")

##### technique type 
**use** : -t, --technique [index]
| Index      | technique |
| :--------: | --------- |
| 1          | LSB       |
| 2          | Hexdump   |


##### Reference
- [Image Steganography with Python by Stephanie Werli](https://medium.com/@stephanie.werli/image-steganography-with-python-83381475da57 "Image Steganography")
