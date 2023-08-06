import setuptools
from numpy.distutils.core import setup, Extension


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

#---------------------------------------------------------------------------  
ext1 = Extension(
    name='hawkroutines',
    sources=['Root/hawkroutines.f',
             'Root/weightandoptobs.f'],
    f2py_options=["--quiet"],
)

#--------------------------------------------------------------------------
setup(
    name='vbfcprw',
    version='0.2',
    ext_modules=[ext1],
    packages=['vbfcprw'],
    install_requires=["numpy>=1.21.1", "pylorentz", "parton"],
    author="David Hohn",
    author_email="hohn.david@gmail.com",
    url="https://github.com/dhohn/vbfcprw",
    description="wrapper for simplified CP reweighting using HAWK generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    # package_data={
    #     "vbfcprw": ["vbfcprw/data/CT10/CT10.info",
    #                 "vbfcprw/data/CT10/CT10_0000.dat"]
    # },
    # I think the above doesnt work because of the numpy.distutils flavour, but not sure.
    data_files=[("vbfcprw/data/CT10", ["vbfcprw/data/CT10/CT10.info",
                                       "vbfcprw/data/CT10/CT10_0000.dat"])
                ],
    classifiers=["Intended Audience :: Science/Research",
                 "License :: OSI Approved :: MIT License",
                 "Programming Language :: Fortran",
                 "Topic :: Scientific/Engineering :: Physics"],
    license="MIT",
)
