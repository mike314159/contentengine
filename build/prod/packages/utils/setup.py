from setuptools import setup

setup(
    name="utils",
    version="1.0",
    description="A collection of utliity modules",
    author="Mike Elliott",
    author_email="",
    packages=["utils"],
    install_requires=[
        "pandas",
        "psycopg2-binary",
        "pytest",
        "resend"
    ],
)
