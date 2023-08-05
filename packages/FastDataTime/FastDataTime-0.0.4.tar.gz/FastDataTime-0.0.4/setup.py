import setuptools

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="FastDataTime", # Replace with your own package name
    version="0.0.4",
    author="PYmili",
    author_email="mc2005wj@163.com",
    description="Library for fast time output",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codechina.csdn.net/qq_53280175/fastdatatime",
    packages=setuptools.find_packages(),
    classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
