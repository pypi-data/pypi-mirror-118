from setuptools import setup, find_packages

from mir import version

print(version.__version__)

# Module dependencies
requirements = []
with open('requirements.txt') as f:
    for line in f.read().splitlines():
        requirements.append(line)

setup(
    name='pymir',
    version=version.__version__,
    python_requires=">=3.7.8",
    author="Scalable AI Team, Intellifusion",
    author_email="ymir-team@intellif.com",
    description="mir: A data version control tool for Ymir",
    url="http://192.168.70.8/scalable-ai/ymir",
    packages=find_packages(exclude=["*tests*"]),
    install_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["mir = mir.main:main"]},
)
