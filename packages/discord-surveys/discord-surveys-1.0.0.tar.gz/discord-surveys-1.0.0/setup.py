import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

pkg_name = "discord-surveys"

setuptools.setup(
    name=pkg_name,
    version="1.0.0",
    author="refekt",
    description="A survey object that utilizes discord.py and discord-interactions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/refekt/discord-surveys",
    project_urls={
        "Bug Tracker": "https://github.com/refekt/discord-surveys/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": pkg_name},
    packages=setuptools.find_packages(where=pkg_name),
    python_requires=">=3.7",
)
