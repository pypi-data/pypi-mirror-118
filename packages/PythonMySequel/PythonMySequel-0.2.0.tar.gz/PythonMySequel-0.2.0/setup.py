import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="PythonMySequel",
    version="0.2.0",
    author="Jason Li",
    description="An easier to use MySQL/SQLite connector for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/jasonli0616/PythonMySequel",
    project_urls={
        "Bug Tracker": "https://github.com/jasonli0616/PythonMySequel/issues",
    },
    package_dir={"":"pythonmysequel"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)