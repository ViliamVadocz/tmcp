from distutils.core import setup

setup(
    name="tmcp",
    packages=["tmcp"],
    version="0.5",
    license="MIT",
    description="Helper classes for the Team Match Communication Protocol.",
    author="Viliam Vadocz",
    author_email="viliam.vadocz@gmail.com",
    url="https://github.com/ViliamVadocz/tmcp/",
    download_url="https://github.com/ViliamVadocz/tmcp/archive/v_05.tar.gz",
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
