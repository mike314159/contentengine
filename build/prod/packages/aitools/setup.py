from setuptools import setup

setup(
    name="aitools",
    version="1.0",
    description="A collection of AI tools",
    author="Mike Elliott",
    author_email="",
    packages=["aitools"],
    install_requires=[
        "pandas",
        "psycopg2-binary",
        "pytest",
        "openai",
        "chromadb",
        "langchain"
    ],
)
