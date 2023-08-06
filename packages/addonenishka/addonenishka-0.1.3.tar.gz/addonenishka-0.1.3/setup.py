import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="addonenishka",
    version="0.1.3",
    author="Nishka Arora",
    author_email="naarora@caltech.edu",
    description="Add one example package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NishkaArora/packagingtutorial",
    # project_urls={
        # "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"addonenishka": "src/examplepackagenishka"},
    packages=setuptools.find_packages(where="src/examplepackagenishka"),
    package_data={'addonenishka':['data/*.csv']},
    python_requires=">=3.6",
    install_requires=['pandas', 'numpy'],
    entry_points = {
        'console_scripts': ['addone=examplepackagenishka.example:main']
    }
)