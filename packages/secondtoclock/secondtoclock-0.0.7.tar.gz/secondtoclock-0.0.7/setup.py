from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='secondtoclock',
    version='0.0.7',
    author="LulubelleIII",
    author_email="<uytudef@gmail.com>",
    description='A package to convert seconds to clock',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['python', 'time', 'clock',
              'seconds to clock', 'time converter'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
