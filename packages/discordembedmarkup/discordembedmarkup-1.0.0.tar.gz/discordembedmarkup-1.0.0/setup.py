import setuptools


with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()


setuptools.setup(
    name="discordembedmarkup",
    version="1.0.0",
    author="xImAnton_",
    description="Declarative Discord Embeds",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/xImAnton/Discord-Embed-Markup",
    project_urls={
        "Bug Tracker": "https://github.com/xImAnton/Discord-Embed-Markup/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.8"
)