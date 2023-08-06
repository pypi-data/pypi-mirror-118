from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='logfly',
    version='0.6',
    packages=['logfly'],
    url='https://github.com/TinQlo/logfly',
    license='MIT License',
    author='Yuan Sui',
    author_email='orisui@icloud.com',
    description='a simple log tool for python',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
