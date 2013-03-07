import distutils.core
import setuptools

distutils.core.setup(
    name="tmdb",
    packages = ["."],
    install_requires = ['requests>=0.11.1'],    
    )