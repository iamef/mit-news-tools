import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mit-news-tools-iamef",  # Replace with your own username
    version="0.0.2",
    author="Arun Wongprommoon and Emily Fan",
    author_email="emilyfan@mit.edu",
    description="tools to help people better understand the news",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.mit.edu/Tegmark-Research-Group/mit-news-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)