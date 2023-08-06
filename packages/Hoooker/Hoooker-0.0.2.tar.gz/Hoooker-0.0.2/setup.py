import setuptools

with open("Hoooker/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='Hoooker',
    version='0.0.2',
    description='Hoooker',
    author='Theta',
    license='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={
        "": ["*.txt", "*.py", "*.md"]
    },
    zip_safe=False
)
