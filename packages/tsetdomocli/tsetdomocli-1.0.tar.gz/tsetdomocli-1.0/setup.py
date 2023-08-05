import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='tsetdomocli',
    version='1.0',
    author='Tianran Wei',
    author_email='weitr.noah@gmail.com',
    description='A cli tool for docker monitoring with prometheus and cAdvisor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'domo = testdomocli.__main__:app'
        ]
    }
)
