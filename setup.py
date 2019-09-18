from distutils.core import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'FasterPay Python3 SDK',
  packages = ['fasterpay'],
  version = '1.0',
  license='MIT',
  description = 'FasterPay Python SDK enables you to integrate the FasterPay’s Checkout Page seamlessly without having the hassle of integrating everything from Scratch. Once your customer is ready to pay, FasterPay will take care of the payment, notify your system about the payment and return the customer back to your Thank You page.',
  long_description = long_description,
  author = 'FasterPay Integration Team',
  author_email = 'integration@fasterpay.com',
  url = 'https://github.com/FasterPay/fasterpay-python',
  download_url = 'https://github.com/FasterPay/fasterpay-python/releases',
  keywords = ['FASTERPAY', 'PAYMENTS', 'CARD PROCESSING'],
  install_requires=['requests']
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Payment Gateway',
    'License :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)