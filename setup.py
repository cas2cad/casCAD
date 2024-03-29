import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(name='cascadv2',
      version='0.1', description='A compute governance tools', author='will holden', long_description=README,
      long_description_content_type='text/markdown',
      url='https://github.com/cas2cad/casCAD',
      packages=['cascad'], author_email="rembern@126.com", include_package_data=True, install_requires=['mesa', 'owlready2'],
      entry_points={
          "console_scripts": [
              "cascad=cascadcli.__main__:main"
          ]
      }
      )