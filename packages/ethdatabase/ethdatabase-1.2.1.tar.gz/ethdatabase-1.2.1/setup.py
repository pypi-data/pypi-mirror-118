from setuptools import setup

setup(
    name='ethdatabase',
    version="1.2.1",
    author="Alberto Pirillo",
    packages=["ethdatabase"],
    install_requires=["mysql-connector-python~=8.0.26", "PyYAML~=5.4.1"],
    python_requires=">=3.6"
)
