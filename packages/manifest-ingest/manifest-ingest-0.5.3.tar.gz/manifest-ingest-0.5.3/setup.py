#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

from setuptools import setup


def get_version(*file_paths):
    """Retrieves the version from manifest/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )  # noqa
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("manifest", "__init__.py")

readme = open("README.md").read()
history = open("HISTORY.md").read()
requirements = open("requirements.txt").readlines()

setup(
    name="manifest-ingest",
    version=version,
    description="""Download a project JSON manifest and its media files via SFTP, HTTP or Amazon S3. This tool was developed for internal use on all X Studios interactive installations which need to have the ability to run "offline" when there is no active network connection.""",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    author="Tim Santor",
    author_email="tsantor@xstudios.com",
    url="https://bitbucket.org/xstudios/manifest-ingest",
    packages=[
        "manifest",
    ],
    # packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    include_package_data=True,
    package_data={},
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords="ftp manifest downloader",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "manifest-ingest = manifest.main:run",
            "manifest-sftp = manifest.main:run",
            "manifest-http = manifest.main:run",
            "manifest-s3 = manifest.main:run",
        ],
    },
)
