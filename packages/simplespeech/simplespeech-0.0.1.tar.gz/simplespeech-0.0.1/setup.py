from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Simple Speech'
LONG_DESCRIPTION = 'A package for speech recognition which works without Pyaudio Note: Internet connection is necessary'

# Setting up
setup(
    name="simplespeech",
    version=VERSION,
    author="Ayush Dubey",
    author_email="usaksham01@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['stt', 'simplespeech', 'speech', 'ayushdubey'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
