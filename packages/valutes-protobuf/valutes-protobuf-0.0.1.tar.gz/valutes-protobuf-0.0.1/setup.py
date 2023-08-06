import setuptools


setuptools.setup(
    name="valutes-protobuf",
    version="0.0.1",
    author="Oleg Tolkachev",
    author_email="blockbusted.dev@gmail.com",
    description="Protobuf-files for VisorLabs test task.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[],
    entry_points={
        "console_scripts": [
            "init_proto_configs=init_proto_configs:main",
        ]
    },
    include_package_data=True
)
