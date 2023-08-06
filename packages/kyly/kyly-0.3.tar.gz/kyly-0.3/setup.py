import setuptools as x

with open('README.md') as f:
    long_description = f.read()

x.setup(
    name='kyly',
    version='0.03',
    author='Siddhant Kumar',
    description='Simple API wrapper for bit.ly',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=x.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
    py_modules=['kyly'],
    package_dir={'':'kyly/src'},
    install_requires=[]
)
