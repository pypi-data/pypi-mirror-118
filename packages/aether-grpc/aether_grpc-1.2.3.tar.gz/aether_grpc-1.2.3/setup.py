from setuptools import setup, find_packages

setup(
    name="aether_grpc",
    description="Aether GRPC definitions",
    version="1.2.3",
    author="Calum Webb",
    author_email="calumpeterwebb@icloud.com",
    url="https://github.com/aether-labs/aether-grpc",
    download_url="https://github.com/aether-labs/aether-grpc/archive/refs/tags/1.2.3.tar.gz",
    keywords=["aether", "aether-grpc", "grpc"],
    packages=find_packages(),
    install_requires=[
        "grpcio==1.39.0",
    ],
    extras_require={
        "dev": [
            "grpcio-tools==1.39.0",
            "black==21.8b0",
            "bump2version==1.0.1",
            "ipdb==0.13.9",
            "twine==3.4.2",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
