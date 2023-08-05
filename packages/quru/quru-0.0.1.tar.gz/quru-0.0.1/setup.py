import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quru",
    version="0.0.1",
    author="Shen Han",
    description="A Python workflow framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    download_url = "https://github.com/ShawnHan1993/quru/archive/refs/tags/0.0.1.tar.gz",
    url = "https://github.com/ShawnHan1993/quru",
    python_requires='>=3.7',
    install_requires=[
        "pika==1.1.0",
        "mongoengine==0.23.1",
        "aiozipkin==0.6.0",
        "aio-pika==5.6.3",
        "structlog==20.1.0",
        "redis==3.2.1"
    ]
)