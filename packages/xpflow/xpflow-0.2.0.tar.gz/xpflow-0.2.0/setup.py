from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='xpflow',
      version='0.2.0',
      description='Utilities for representing experiments',
      url='https://github.com/sileod/xpflow',
      author='sileod',
      license='MIT',
      install_requires=['easydict'],
      download_url='https://github.com/sileod/xpflow/archive/refs/tags/V0.2.tar.gz',
      py_modules=['xpflow'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
