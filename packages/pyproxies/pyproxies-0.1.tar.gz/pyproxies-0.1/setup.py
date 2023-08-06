from setuptools import setup, find_packages
 
classifiers = [
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Education",
  "Operating System :: Microsoft :: Windows :: Windows 10",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3.9"
]
 
setup(
  name="pyproxies",
  version="0.1",
  description="Python proxy scraper module, only returns valid proxies whose timeout is less than 10 seconds.",
  long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
  url="https://github.com/venaxyt/pyproxies",  
  author="Venax",
  author_email="venaxumofficial@gmail.com",
  license="MIT",
  keywords="pyproxies",
  classifiers=classifiers,
  install_requires=["requests"],
  packages=["pyproxies"]
)