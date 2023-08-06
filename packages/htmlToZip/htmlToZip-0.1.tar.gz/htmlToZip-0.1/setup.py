import setuptools

setuptools.setup(
    name="htmlToZip",
    version=0.1,
    author="Mahendra kumar",
    author_email="mksuthar9016@gmail.com",
    description="Convert your html, css and js code into project",
    long_description="this is desc",
    long_description_content_type="text/markdown",
    url="https://github.com/mahendra-suthar/html-to-url",
    project_urls={
        "Bug Tracker": "https://github.com/mahendra-suthar/html-to-url/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "html_to_url"},
    packages=setuptools.find_packages(where="html_to_url"),
    python_requires=">=3.6",
)
