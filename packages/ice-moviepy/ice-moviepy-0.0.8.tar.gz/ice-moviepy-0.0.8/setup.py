#!/usr/bin/env python
"""MoviePy setup script."""

import os
import sys
from codecs import open


try:
    from setuptools import find_packages, setup
    from setuptools.command.test import test as TestCommand
except ImportError:
    try:
        import ez_setup

        ez_setup.use_setuptools()
    except ImportError:
        raise ImportError(
            "Ice-MoviePy could not be installed, probably because "
            "neither setuptools nor ez_setup are installed on this computer.\n"
            "Install setuptools with $ (sudo) pip install setuptools and "
            "try again."
        )


# class PyTest(TestCommand):
#     """Handle test execution from setup."""

#     user_options = [("pytest-args=", "a", "Arguments to pass into pytest")]

#     def initialize_options(self):
#         """Initialize the PyTest options."""
#         TestCommand.initialize_options(self)
#         self.pytest_args = ""

#     def finalize_options(self):
#         """Finalize the PyTest options."""
#         TestCommand.finalize_options(self)
#         self.test_args = []
#         self.test_suite = True

#     def run_tests(self):
#         """Run the PyTest testing suite."""
#         try:
#             import pytest
#         except ImportError:
#             raise ImportError(
#                 "Running tests requires additional dependencies.\n"
#                 "Please run $ pip install moviepy[test]"
#             )

#         errno = pytest.main(self.pytest_args.split(" "))
#         sys.exit(errno)


# cmdclass = {"test": PyTest}  # Define custom commands.

# if "build_docs" in sys.argv:
#     try:
#         from sphinx.setup_command import BuildDoc
#     except ImportError:
#         raise ImportError(
#             "Running the documentation builds has additional dependencies.\n"
#             "Please run $ pip install moviepy[doc]"
#         )

#     cmdclass["build_docs"] = BuildDoc


# Define the requirements for specific execution needs.
requires = [
    "decorator==4.4.2",
    "imageio==2.9.0",
    "imageio_ffmpeg==0.4.5",
    "numpy==1.21.2",
    "proglog==0.1.9",
    "Pillow==8.1.0",
    "pysrt==1.1.2",
]

optional_reqs = [
    "pygame>=1.9.3",
    "python-dotenv>=0.10",
    "opencv-python",
    "scikit-image",
    "scikit-learn",
    "scipy",
    "matplotlib",
    "youtube_dl",
]

doc_reqs = [
    "numpydoc<2.0",
    "Sphinx==3.4.3",
    "sphinx-rtd-theme==0.5.1",
]

test_reqs = [
    "coveralls>=3.0,<4.0",
    "pytest-cov>=2.5.1,<3.0",
    "pytest>=3.0.0,<7.0.0",
]

lint_reqs = [
    "black>=20.8b1",
    "flake8>3.7.0,<4.0.0",
    "flake8-absolute-import>=1.0",
    "flake8-docstrings>=1.5.0",
    "flake8-rst-docstrings>=0.0.14",
    "flake8-implicit-str-concat==0.2.0",
    "isort>=5.7.0",
    "pre-commit>=2.9.3",
]

extra_reqs = {
    "optional": optional_reqs,
    "doc": doc_reqs,
    "test": test_reqs,
    "lint": lint_reqs,
}

# Load the README.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__="0.0.8"

setup(
    name="ice-moviepy",
    version=__version__,
    author="Haj mammad",
    author_email="mbxeby@hi2.in",
    description="a package for extracting short subtitled clips from movies by subtitle.srt file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Video :: Capture",
        "Topic :: Multimedia :: Video :: Conversion",
    ],
    keywords="cut clip logo video editing audio compositing ffmpeg",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    command_options={
        "build_docs": {
            "build_dir": ("setup.py", "./docs/build"),
            "config_dir": ("setup.py", "./docs"),
            "version": ("setup.py", __version__.rsplit(".", 2)[0]),
            "release": ("setup.py", __version__),
        }
    },
    tests_require=test_reqs,
    install_requires=requires,
    extras_require=extra_reqs,
)