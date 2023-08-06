from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION = '0.0.37'

# Setting up
setup(
    name="prism_rerun",
    version=VERSION,
    author="Ashwin Kumar",
    author_email="<ashwinkumar@chargebee.com>",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
            'console_scripts': [
                    'cb-rerun = prism_rerun.prism_rerun.__main__:main'
            ]
    },
)