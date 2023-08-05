from traceback import extract_tb

import setuptools
from os import path

# with open("./README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="Natasy",
    version="0.0.1",
    author="Mohamed",
    author_email="mohamed@eldesouki.com",
    description="A machine learning engine designed and developed to be both easy to use and source code readable.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/disooqi/Natasy",
    project_urls={
        "Bug Tracker": "https://github.com/disooqi/Natasy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Academic Free License (AFL)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src",
                                      exclude=[
                                          'docs', 'tests'
                                      ]),
    install_requires=['numpy>=1.21.2',
                      'scipy>=1.7.1',
                      'tqdm>=4.62.2'],
    python_requires=">=3.6",
    extras_require=dict(tests=['pytest'])

)
