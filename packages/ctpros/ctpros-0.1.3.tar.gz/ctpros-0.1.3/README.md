# ctpros: Computed Tomography Processing & Registration - Open Sourced <!-- omit in toc -->
[![License-GPLv3](https://img.shields.io/badge/license-GPLv3-lightgrey)](https://www.gnu.org/licenses/gpl-3.0)
[![version](https://img.shields.io/pypi/v/ctpros?color=green&label=version)](https://gitlab.com/caosuna/ctpros/)
[![downloads](https://img.shields.io/pypi/dm/ctpros?color=g&label=downloads)](https://pypi.org/project/ctpros/)
[![Docs-Sphinx](https://img.shields.io/badge/docs-sphinx-blue)](https://caosuna.gitlab.io/ctpros)
[![coverage](https://img.shields.io/gitlab/coverage/caosuna/ctpros/master)](https://gitlab.com/caosuna/ctpros/-/jobs/artifacts/master/file/.artifacts/coverage/coverage_html/index.html?job=coverage)

[![python-3.7](https://img.shields.io/badge/python-3.7-yellow)](https://www.python.org/downloads/release/python-379/)
[![code style: black](https://img.shields.io/badge/code_format-black-black)](https://github.com/psf/black)
[![testing-unittest](https://img.shields.io/badge/testing-unittest-orange)](https://docs.python.org/3/library/unittest.html)
[![coverage-coverage.py](https://img.shields.io/badge/coverage-coverage.py-green)](https://github.com/nedbat/coveragepy)
[![PyPI](https://img.shields.io/badge/deployment-PyPI-black)](https://pypi.org)


A handy graphic user interface (GUI) and application programming interface (API) to apply common imaging techniques to your research images.

<img src="docs/images/guiexample.png">
Two micro-CT images of a single specimen are shown following precise registration of their overlapping region before stitching.

## Summary <!-- omit in toc -->
This program's goal is to ease the utilization of Python's powerful imaging libraries in medical imaging research, particularly with micro-computed tomography. By introducing affine matrices and subvolumes to raw image data, linear mappings and scaled metrics can be defined between images of varying resolutions, easing common image processing pipelines. The UI permits intuitive dragging and rotating along points and orthogonal cross-sections to help you visualize and align your data!
## Index <!-- omit in toc -->
- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)

## Installation
###  Scripts <!-- omit in toc -->
Not familiar with Python? Download and run the following script installer for:
  
- [Windows](bin/ctpros_wininstaller.bat)

  The download button is to the right-most side of the file header:

  ![image-info](docs/images/download_script.PNG)
- Note: Windows may be careful and prompt you to verify to run the script. Select **More Info** then **Run anyway**

  <img src = "docs/images/winsafety.PNG" width=300>


Familiar with Python? Just `pip install ctpros` in your Python 3.7 virtual environment with the below system requirements:
- For all operating systems:
  - [Python 3.7 64-bit](https://www.python.org/downloads/release/python-379/)
    - ITK version used is released only for 3.7.
- For headless servers utilizing graphics/graphic commands:
  - `xvfb`
    - X virtual frame buffer to mimic a screen
  - OpenGL
    - Open-sourced graphics library (`libgl1-mesa-dev`)
  
##  Usage
Use either the graphic application for your general visualization and image manipulation needs or use the API for scripting, batching, or specifying pipelines. See below for your use case:

### Graphic User Interface <!-- omit in toc -->
Using one of the installer scripts generates a `ctpros.bat` in the directory of the installer script. Run the generated `ctpros.bat` to call the program.

For those familiar with Python, call `ctpros` as a module within the Python virtual environment: `python -m ctpros`

For detailed controls, see the [GUI Controls Guide](docs/helpme_guicontrols.md).

### Application Programming Interface <!-- omit in toc -->
Import `ctpros` like any other Python module to access the GUI and NumPy-derived image classes. Be sure to use the virtual environment `ctpros` is installed in to be able to import it.
```python
import ctpros

myaim = ctpros.AIM(shape=(50,50,50),dtype='int16')
```
See the [notebooks](notebooks/notebooks.MD) and [automated source code documentation](https://caosuna.gitlab.io/ctpros) for more examples of API usage.

## Contributors
See [CONTRIBUTING.md](CONTRIBUTING.md) for code requirements and structure, pipeline details, and more.

## License
[GPL 3.0](LICENSE.txt)
