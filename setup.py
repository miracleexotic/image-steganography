from setuptools import setup

setup(
    name='steganography',
    version='0.1.0',
    py_modules=['Steganography'],
    install_requires=[
        'click',
        'numpy',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'steganography = Steganography:cli',
        ],
    },
)