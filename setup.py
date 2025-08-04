import os
from setuptools import setup

def read(fname):
  return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
  name='fasterpay-python3',
  version='1.2',
  packages=['fasterpay'],
  description='Faster Python Library',
  long_description=read('pypi_description.rst'),
  license='MIT',
  url='https://github.com/FasterPay/fasterpay-python3',
  download_url='https://github.com/FasterPay/fasterpay-python3/releases',
  author='FasterPay Integrations Team',
  author_email='integration@fasterpay.com',
  keywords=['FASTERPAY', 'PAYMENTS', 'CARD PROCESSING'],
  install_requires=['requests'],
  python_requires=">=3.6",
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)