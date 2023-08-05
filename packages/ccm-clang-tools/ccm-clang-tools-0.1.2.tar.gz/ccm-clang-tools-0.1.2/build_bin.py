from setuptools import Extension, find_packages
from setuptools.dist import Distribution

class CCMToolsDist(Distribution):
    def has_ext_modules(*args, **kwargs):
        return True


def build(setup_kwargs):
    setup_kwargs.update(
            distclass=CCMToolsDist
            )
    return

