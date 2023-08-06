import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TagsAsADatabase",
    version="0.0.4",
    author="Oren Leung",
    author_email="ok2leung@uwaterloo.ca",
    description="Use AWS Tags As A Key-Value DataBase",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OrenLeung/AWSTagsAsADatabase",
    project_urls={
        "Bug Tracker": "https://github.com/OrenLeung/AWSTagsAsADatabase/issues",
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "boto3"
    ],


    python_requires=">=3.6",
)
