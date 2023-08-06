from setuptools import setup

try:
    from Cython.Build import cythonize
except ImportError:
    cythonize = None

with open("requirements.txt") as fp:
    install_requires = fp.read().strip().split("\n")

setup(
    name='discord.pyx',
    version = '0.0.0',
    license = 'MIT',
    description = 'Cython wrapper for Discord',
    install_requires=install_requires,
    ext_modules=cythonize("discord/*.pyx")
)