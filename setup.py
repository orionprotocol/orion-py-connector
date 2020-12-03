from setuptools import find_packages, setup

setup(name='orion-py-connector',
      version='0.1',
      description='',
      url='https://github.com/orionprotocol/orion-py-connector',
      author='Simon Kruse',
      author_email='simon@orionprotocol.io',
      license='MIT',
      packages=['orion_py_connector'],
      install_requires=[
          'requests',
          'eip712-structs',
          'web3'
      ],
      zip_safe=False)
