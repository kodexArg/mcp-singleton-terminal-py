#!/usr/bin/env python3
"""
Setup script para terminal-singleton-py
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="terminal-singleton-py",
    version="1.0.0", 
    author="Kodex",
    description="Librería Python para interactuar con la terminal usando un patrón singleton",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kodex/terminal-singleton-py",
    packages=["terminal_singleton"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    keywords=["terminal", "singleton", "zsh", "pexpect", "shell", "automation"],
    project_urls={
        "Repository": "https://github.com/kodex/terminal-singleton-py", 
        "Documentation": "https://github.com/kodex/terminal-singleton-py#readme",
    },
) 