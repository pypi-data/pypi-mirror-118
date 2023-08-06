from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ProfiTrade',
    version='0.0.4',
    description='A proprietary open source fintech python package with a plethora of features for building equity and cryptocurrency trading algorithms.',
    long_description=long_description,
    url='https://github.com/harrisiva/ProfiTrade-Package',
    author='Harriharan Sivakumar',
    author_email='harrishiv6@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Trading, Stock, Algorithmic Trading, Quantitative, Crypto',
    packages=find_packages(),
    install_requires=['']
)
