from setuptools import setup

setup(
    name='print_test_module',
    version='1.0',
    description='print test module of PyPI',
    author='ryan',
    author_email='conquerfu@gmail.com',
    url='https://www.python.org/',
    license='MIT',
    packages=['my_test_module'],
    install_requires=['numpy>=1.14'],
    python_requires='>=3'
)