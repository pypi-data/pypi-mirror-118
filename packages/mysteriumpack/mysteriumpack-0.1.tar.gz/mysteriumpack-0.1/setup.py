from setuptools import setup, find_packages
 
classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Education",
  "Operating System :: Microsoft :: Windows :: Windows 10",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3.9"
]
 
setup(
  name="mysteriumpack",
  version="0.1",
  description="@venaxyt",
  long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
  url="https://github.com/venaxyt/mysterium",  
  author="Venax",
  author_email="venaxumofficial@gmail.com",
  license="MIT",
  keywords="mysteriumpack",
  classifiers=classifiers,
  install_requires=["pytest", "pywin32", "pyarmor", "unpy2exe", "uncompyle6"],
  packages=["mysteriumpack"]
)