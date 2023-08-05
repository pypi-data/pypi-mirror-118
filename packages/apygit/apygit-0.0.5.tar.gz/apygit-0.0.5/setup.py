from setuptools import setup, find_packages


long_description = None
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='apygit',
    packages=find_packages(),
    version='0.0.5',
    license='MIT',
    description='Python Git Module',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/angarg/pygit',
    platforms=['linux', 'osx'],
    keywords=['git'],
    author='Anupam Garg',
    author_email='angarg@gmail.com',
    python_requires='~=3.6',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Terminals",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    install_requires=[],
    tests_require=["six==1.16.0"],
    test_suite="tests",

)
