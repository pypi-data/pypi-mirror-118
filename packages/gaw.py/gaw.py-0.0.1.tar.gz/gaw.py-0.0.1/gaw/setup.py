import setuptools


long_description = '# About\n This is a python package/api wrapper for guilded' # Your README.md file will be used as the long description!

setuptools.setup(
    name="gaw.py", # Put your username here!
    version="0.0.1", # The version of your package!
    author="Elian Galdamez", # Your name here!
    author_email="elian.galdamez510@gmail.com", # Your e-mail here!
    description="A package for guilded's api", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://guilded.gg", # Link your package website here! (most commonly a GitHub repo)
    packages=["gaw", "gaw.gaw"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.8', # The version requirement for Python to run your package!
)
