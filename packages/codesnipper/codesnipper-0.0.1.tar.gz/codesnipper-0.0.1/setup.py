# Use this guide:
# https://packaging.python.org/tutorials/packaging-projects/
# from unitgrade2.version import __version__
import setuptools
# with open("src/unitgrade2/version.py", "r", encoding="utf-8") as fh:
#     __version__ = fh.read().split(" = ")[1].strip()[1:-1]
# long_description = fh.read()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="codesnipper",
    version="0.0.1",
    author="Tue Herlau",
    author_email="tuhe@dtu.dk",
    description="A lightweight framework for censoring student solutions files and extracting code + output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://lab.compute.dtu.dk/tuhe/snipper',
    project_urls={
        "Bug Tracker": "https://lab.compute.dtu.dk/tuhe/snipper/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['jinja2',],
)

# setup(
#     name='unitgrade',
#     version=__version__,
#     packages=['unitgrade2'],
#     url=,
#     license='MIT',
#     author='Tue Herlau',
#     author_email='tuhe@dtu.dk',
#     description="""
# A student homework/exam evaluation framework build on pythons unittest framework. This package contains all files required to run unitgrade tests as a student. To develop tests, please use unitgrade_private.
# """,
#     include_package_data=False,
# )
