import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="route53-ddns",
    version="0.0.3",
    author="Enrico Carlesso",
    author_email="enricocarlesso@gmail.com",
    description="A simple package that updated an AWS Route53 A record to point to the current IP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carlesso/route53-ddns",
    project_urls={
        "Bug Tracker": "https://github.com/carlesso/route53-ddns/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    extras_require={
        "test": [
            "black",
            "isort",
            "mypy",
            "pytest",
            "pytest-cov",
        ]
    },
)
