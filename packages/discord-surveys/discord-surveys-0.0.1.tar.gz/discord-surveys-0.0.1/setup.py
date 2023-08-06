import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="discord-surveys",
    version="0.0.1",
    author="refekt",
    author_email="refekt@gmail.com",
    description="A survey object that utilizes discord.py and discord-interactions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/refekt/SlashSurveys",
    project_urls={
        "Bug Tracker": "https://github.com/refekt/SlashSurveys/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)