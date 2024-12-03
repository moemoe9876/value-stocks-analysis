from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='value_stocks_analysis',
    version='0.1.0',
    author='Value Stocks Analysis Team',
    description='Python package for analyzing value stocks using Warren Buffett\'s principles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'yfinance>=0.1.70',
        'requests>=2.26.0',
        'python-dotenv>=0.19.0'
    ],
    python_requires='>=3.7'
)