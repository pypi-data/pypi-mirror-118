from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='secondtoclock',
    version='0.0.3',
    author="LulubelleIII",
    author_email="<uytudef@gmail.com>",
    descriptipn='A package to convert seconds to clock',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
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
