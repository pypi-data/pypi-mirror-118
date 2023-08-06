from setuptools import setup, find_packages
from os.path import abspath, dirname, join

# Fetches the content from README.md
# This will be used for the "long_description" field.
README_MD = open(join(dirname(abspath(__file__)), "README.md")).read()

setup(

    name="dontinstallthislmaoX",


    version="1.0.1",


    packages=find_packages(),

    # The description that will be shown on PyPI.
    # Keep it short and concise
    # This field is OPTIONAL
    description="A small clone of lodash",

    # The content that will be shown on your project page.
    # In this case, we're displaying whatever is there in our README.md file
    # This field is OPTIONAL
    long_description=README_MD,


    long_description_content_type="text/markdown",

    url="https://github.com/railwaysama/hellobitchx",
    # These fields are OPTIONAL
    author_name="railwaysama",
    author_email="elonmusk@btc.com",

    # Classifiers help categorize your project.
    # For a complete list of classifiers, visit:
    # https://pypi.org/classifiers
    # This is OPTIONAL
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only"
    ],

    # Keywords are tags that identify your project and help searching for it
    # This field is OPTIONAL
    keywords="lodash, string, manipulation",

)
