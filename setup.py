from distutils.core import setup


setup(
    name="warepy",
    packages=["warepy"],
    version="0.2.0",
    license="MIT",
    description="My toolkit for Python.",
    author = "Alexander Ryzhov",
    author_email = "thed4rkof@gmail.com",
    url = "https://github.com/ryzhovalex/warepy",
    download_url = "https://github.com/ryzhovalex/warepy/archive/refs/tags/0.2.0.tar.gz",
    keywords = ["toolkit", "python-core"],
    install_requires=[
        "yaml",
        "loguru"
    ],
    classifiers=[
        "Development Status :: 1 - Planning",

        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3.9",
    ],
)