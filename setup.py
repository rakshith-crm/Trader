from setuptools import setup, find_packages

with open('README.md') as file:
    description = file.read()

setup(
    name="traderpy",
    version="1.0.6",
    packages=find_packages(),
    install_requires=[
        'yfinance',
        'pandas',
        'pygame',
        'plotly',
        'tqdm',
        'scikit-learn',
        'scipy',
        'numpy',
        'tabulate'
    ],
    long_description=description,
    long_description_content_type="text/markdown"
)