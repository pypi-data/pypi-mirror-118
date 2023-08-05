import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YouTubeMusicAPI",
    version="2.1",
    author="Sijey Praveen",
    author_email="cjpraveen@hotmail.com",
    description="An unofficial YouTube Music API For Python Programming Language.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sijey-Praveen/YouTube-Music-API",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords = "youtube music api, YouTubeMusicAPI, python youtube music api, youtube api pypi,sijey-praveen pypi, youtube api, sijey, sijey-praveen, sijey praveen projects",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
