import setuptools
import robo_cop as rc

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name=rc.APP_NAME,
    version=rc.APP_VERSION,
    author=rc.APP_AUTHOR,
    license=rc.APP_LICENSE,
    description=rc.APP_DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=rc.APP_URL,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "twitch-python >= 0.0.19"
    ],
    extras_require={
        "dev": [
            "setuptools",
            "wheel",
            "flake8",
            "twine",
            "sphinx",
            "sphinx_rtd_theme",
        ]
    },
    python_requires='>=3.9.0',
    entry_points={
        "console_scripts": [
            f'{rc.APP_NAME} = robo_cop.__main__:main'
        ]
    }
)
