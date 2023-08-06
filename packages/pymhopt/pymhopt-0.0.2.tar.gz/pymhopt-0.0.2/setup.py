import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pymhopt',
    version='0.0.2',
    scripts=['pymhopt_package'],
    install_requires=[
        "pandas",
        "numpy",
        "gplearn",
        "scikit_learn",
        "matplotlib",
        "graphviz",
    ],
    author="Ajay Arunachalam",
    author_email="ajay.arunachalam08@gmail.com",
    description="Python Wrapper for Optimization Algorithms",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url='https://github.com/ajayarunachalam/pymhopt/',
    packages=setuptools.find_packages(),
    py_modules=['pyOP/optimization', 'pyOP/SKLearnInterface', 'pyOP/Evolution/Evolution', 'pyOP/Fitness/FitnessFunction','pyOP/Nodes/BaseNode', 'pyOP/Nodes/SymbolicRegressionNodes','pyOP/Selection/Selection', 'pyOP/Variation/Variation'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

)
