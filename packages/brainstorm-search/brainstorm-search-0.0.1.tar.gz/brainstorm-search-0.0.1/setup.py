import setuptools
long_desc = open("README.md").read()
required = ["setuptools>=42", "wheel", "beautifulsoup4", "duckduckgo_search"]
setuptools.setup(
    name="brainstorm-search",
    version="0.0.1",
    author="Jonathan Li",
    license="MIT License",
    entry_points={
        'console_scripts': ['brainstorm=brainstorm_search.main:main'],
    },
    description="Summarize idea lists from Duckduckgo. Make idea brainstorming efficient.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/jnbli/brainstorm-search",
    project_urls={
        "Bug Tracker": "https://github.com/jnbli/brainstorm-search/issues",
    },
    install_requires=required,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
