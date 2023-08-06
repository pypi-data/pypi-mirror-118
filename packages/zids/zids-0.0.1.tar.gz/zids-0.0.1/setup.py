import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zids",
    version="0.0.1",
    author="Zach Gulde",
    author_email="zachgulde@gmail.com",
    description="Create interactive documentation documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zgulde/zids",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "jinja2>=3",
        "markdown>=3",
        "markdown-full-yaml-metadata>=2",
    ],
    entry_points={"console_scripts": ["zids = zids.zids:main"]}
)
