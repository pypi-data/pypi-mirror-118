import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyjazzclient",
    version="0.0.1",
    author="Steve Wallace",
    author_email="gnomerspell@gmail.com",
    description="Python package for interacting with IBM Jazz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnomerspell/pyjazzclient",
    project_urls={
        "Issues": "https://github.com/gnomerspell/pyjazzclient/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    packages=["pyjazzclient"],
    install_requires=[
        'requests'
    ]
)
