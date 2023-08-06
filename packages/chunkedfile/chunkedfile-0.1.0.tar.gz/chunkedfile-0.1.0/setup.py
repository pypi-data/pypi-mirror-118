import setuptools
import pathlib


setuptools.setup(
    name='chunkedfile',
    version='0.1.0',
    description='Mastering Atari with Discrete World Models',
    url='http://github.com/danijar/chunkedfile',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['chunkedfile'],
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
