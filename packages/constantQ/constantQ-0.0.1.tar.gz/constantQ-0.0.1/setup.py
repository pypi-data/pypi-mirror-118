import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="constantQ", 
    version="0.0.1",
    author="Xiyuan Li",
    author_email="xli2522@uwo.ca",
    description="constantQ: Constant Q Transform with minimal size and dependencies based on GWpy qtransform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU',
    url="https://xli2522.github.io/Constant-Q/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
