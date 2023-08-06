import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-gooaye",
    version="0.0.1",
    author="Blue",
    author_email="iamjasonlan@gmail.com",
    description="Scrapy spider for Gooaye Website",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bluesss30/Gooaye",
    install_requires=[
        'Scrapy>=1'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # package_dir={"": "src"},
    packages=setuptools.find_packages(), # (where="src"),
    python_requires=">=3.6",
)