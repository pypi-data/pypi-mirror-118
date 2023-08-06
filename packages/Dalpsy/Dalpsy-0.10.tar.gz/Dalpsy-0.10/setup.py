import setuptools as x

with open('README.md') as f:
    long_description = f.read()

x.setup(
    name='Dalpsy',
    version='0.10',
    author='Siddhant Kumar',
    description='Anime, Manga API wrapper for Anime-Planet',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=x.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    py_modules=['Dalpsy'],
    package_dir={'':'Dalpsy/src'},
    install_requires=['bs4']
)
