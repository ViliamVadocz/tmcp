from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="tmcp",
    packages=["tmcp"],
    version="0.7.1",
    license="MIT",
    description="Helper classes for the Team Match Communication Protocol.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Viliam Vadocz",
    author_email="viliam.vadocz@gmail.com",
    url="https://github.com/ViliamVadocz/tmcp/",
    download_url="https://github.com/ViliamVadocz/tmcp/archive/v_0_7_1.tar.gz",
    keywords=["RLBot", "protocol"],
    install_requires=["rlbot"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
