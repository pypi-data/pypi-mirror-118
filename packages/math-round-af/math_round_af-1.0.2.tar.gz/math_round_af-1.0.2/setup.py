import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["pylint-af==1.0.1", "pytest==6.2.5"]

setuptools.setup(
    name="math_round_af",
    version="1.0.2",
    author="Albert Farkhutdinov",
    author_email="albertfarhutdinov@gmail.com",
    description=(
        "Python package that allows to get "
        "mathematically rounded floating numbers."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertFarkhutdinov/math_round_af",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
