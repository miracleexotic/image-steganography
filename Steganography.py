import numpy as np
from PIL import Image
import re
import click


class Steganography():
    algor = 1
    delimiter = '#####'

    def __init__(self, img_cover=None, message=None, img_secrete=None) -> None:
        self.img_cover = img_cover
        self.message = message
        self.img_secrete = img_secrete
    
    def _getImgData(self, img):
        try:
            with Image.open(img) as img:
                self.width, self.height = img.size
                self.data = np.array(img)
            return True
        except Exception as e:
            print(f"\033[91m[!] file not Found : {e}\033[00m")
            return False

    @classmethod
    def LSB(cls, img_cover, message, img_secrete):
        Steganography.algor = 1
        return cls(img_cover, message, img_secrete)

    def _encode_LSB(self):
        print("[*] LSB substitution technique encoding...")
        print("[+] Adding delimiter")
        msg = self.message + Steganography.delimiter
        bit_message = ''.join([f"{ord(character):08b}" for character in msg])
        bit_message = [int(bit) for bit in bit_message]
        bit_message_lenght = len(bit_message)
        print(f"[*] bit message lenght : \033[93m{bit_message_lenght}\033[00m")

        if not self._getImgData(self.img_cover):
            return

        self.data = np.reshape(self.data, self.width*self.height*3)
        print(f"[*] Maximun bit (bit data) : \033[93m{len(self.data)}\033[00m")

        if len(self.data) < bit_message_lenght:
            raise ValueError("\033[91m[!] Insufficient bytes, need bigger image or less data.\033[00m")
        
        self.data[:bit_message_lenght] = self.data[:bit_message_lenght] & ~1 | bit_message

        self.data = np.reshape(self.data, (self.height, self.width, 3))

        print("[+] Save image")
        new_img = Image.fromarray(self.data)
        new_img.save(self.img_secrete)
        print("[*] Complete")


    def _decode_LSB(self):
        print("[*] LSB substitution technique decoding...")
        if not self._getImgData(self.img_secrete):
            return

        self.data = np.reshape(self.data, self.width*self.height*3)
        self.data = self.data & 1
        self.data = np.packbits(self.data)

        print("[*] checking delimiter...")
        try:
            secrete = ''.join(filter(lambda x: True if x.isprintable() else False, [chr(i) for i in self.data]))
            secrete = secrete[:secrete.index(Steganography.delimiter)]
        except Exception as e:
            raise ValueError(f"\033[91m[!] Cann't find delimiter : {e}\033[00m")

        print(f"[*] Secrete message : \033[92m{secrete}\033[00m")
        print("[*] Complete")
        return secrete

    @classmethod
    def Hexdump(cls, img_cover, message, img_secrete):
        Steganography.algor = 2
        return cls(img_cover, message, img_secrete)

    def _encode_Hexdump(self):
        print("[*] Hexdump technique encoding...")
        print("[+] Adding delimiter")
        msg = Steganography.delimiter + self.message + Steganography.delimiter
        try:
            with open(self.img_cover, 'rb') as cover, open(self.img_secrete, 'wb') as secrete:
                secrete.write(cover.read())
                secrete.write(msg.encode('utf-8'))
            print("[*] Complete")
        except Exception as e:
            print(f"\033[91m[!] file not Found : {e}\033[00m")

    def _decode_Hexdump(self):
        print("[*] Hexdump technique decoding...")
        try:
            with open(self.img_secrete, 'rb') as data:
                secrete = ''.join([chunk.decode('utf-8', errors="ignore") for chunk in iter(lambda: data.read(8), b'')])
                secrete = re.findall(f'{Steganography.delimiter}.*{Steganography.delimiter}', secrete)[0].strip(Steganography.delimiter)
                print(f"[*] Secrete message : \033[92m{secrete}\033[00m")
            print("[*] Complete")
            return secrete  
        except Exception as e:
            print(f"\033[91m[!] file not Found : {e}\033[00m")       

    def encode(self):
        if Steganography.algor == 1:
            self._encode_LSB()
        elif Steganography.algor == 2:
            self._encode_Hexdump()

    def decode(self, algor=None):
        if not algor:
            algor = Steganography.algor

        if algor == 1:
            return self._decode_LSB()
        elif algor == 2:
            return self._decode_Hexdump()

@click.group()
def cli():
    print('''
  ____  _                                                     _           
 / ___|| |_ ___  __ _  __ _ _ __   ___   __ _ _ __ __ _ _ __ | |__  _   _ 
 \___ \| __/ _ \/ _` |/ _` | '_ \ / _ \ / _` | '__/ _` | '_ \| '_ \| | | |
  ___) | ||  __/ (_| | (_| | | | | (_) | (_| | | | (_| | |_) | | | | |_| |
 |____/ \__\___|\__, |\__,_|_| |_|\___/ \__, |_|  \__,_| .__/|_| |_|\__, |
                |___/                   |___/          |_|          |___/ 
                                                \033[96m[By 3mper0r_ v0.1.0]\033[00m

    ''')

@click.command()
@click.option('-i', '--img-cover', 'img_cover', required=True, help='input image', prompt="Input your image cover file name")
@click.option('-m', '--message', 'message', required=True, help='secrete message', prompt="Input your secrete message")
@click.option('-o', '--img-secrete', 'img_secrete', required=True, help='output image', prompt="Output image file name")
@click.option('-t', '--technique', 'techniqueType', default=1, help='technique for steganography', prompt="choose your technique")
def encode(img_cover, message, img_secrete, techniqueType):
    if techniqueType == 1:
        Steganography.LSB(img_cover, message, img_secrete).encode()
    elif techniqueType == 2:
        Steganography.Hexdump(img_cover, message, img_secrete).encode()

@click.command()
@click.option('-i', '--img-secrete', 'img_secrete', required=True, help='output image', prompt="Input your image file name")
@click.option('-t', '--technique', 'techniqueType', default=1, help='technique for steganography', prompt="choose your technique")
def decode(img_secrete, techniqueType):
    if techniqueType == 1:
        Steganography(img_secrete=img_secrete).decode(1)
    elif techniqueType == 2:
        Steganography(img_secrete=img_secrete).decode(2)

cli.add_command(encode)
cli.add_command(decode)


if __name__ == '__main__':
    # Steganography.LSB('white.png', "3mper0r_pen9uin", 'white-encode.png').encode()
    # Steganography(img_secrete='white-encode.png').decode()

    # Steganography.Hexdump('white.png', "3mper0r_pen9uin love you 3000", 'white-encode.png').encode()
    # Steganography(img_secrete='white-encode.png').decode(2)

    cli()

    

