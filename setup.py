#!/usr/bin/env python
import os
import sys
import subprocess
from glob import glob
import platform

from setuptools import Extension, setup

import versioneer

# define scripts
scripts = ["bin/ginsp", "bin/gconv", "bin/gCache3", "bin/gCatalog3", "bin/gStarform3"]

# find all sub-packages
modules = []
setup_dir = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(setup_dir):
    submod = os.path.relpath(root, setup_dir).replace(os.sep, ".")
    if not submod.startswith("pygad"):
        continue
    if "__init__.py" in files:
        modules.append(submod)

# clean and make the cpygad.so library
# subprocess.run(["make", "clean"], cwd=setup_dir + "/pygad/C", check=True)

gsl_include = ""
gsl_lib = ""
gsl_found = False

if os.getenv("GSL_HOME") is not None:
    gsl_prefix = os.getenv("GSL_HOME")
    gsl_include = os.path.join(gsl_prefix, "include")
    gsl_lib = os.path.join(gsl_prefix, "lib")
    gsl_found = True
else:
    for prefix in [sys.prefix, sys.base_prefix, os.path.join(sys.prefix, ".."), "/usr"]:
        if prefix is None:
            continue
        inc_dir = os.path.join(prefix, "include")
        lib_dir = os.path.join(prefix, "lib")
        if os.path.exists(os.path.join(inc_dir, "gsl", "gsl_integration.h")):
            if (glob(os.path.join(lib_dir, "libgsl.*")) or
                    glob(os.path.join(lib_dir, "libgslcblas.*"))):
                gsl_include = inc_dir
                gsl_lib = lib_dir
                gsl_found = True
                break

if platform.system() == "Windows":
    extra_compile_args = [
        "/O2",  # Optimize for speed
        "/std:c++11",
    ]
    extra_link_args = []
    libraries = ["gsl", "gslcblas"]  # Remove m and gomp which are Unix-specific
else:
    extra_compile_args = [
        "-fPIC",
        "-std=c++11",
        "-O3",
        "-fopenmp",
        "-pedantic",
        "-Wall",
        "-Wextra",
    ]
    extra_link_args = ["-fopenmp"]
    libraries = ["m", "gsl", "gslcblas", "gomp"]

ext_modules = []
if gsl_found:
    ext_module = Extension(
        "pygad/C/cpygad",
        language="c++",
        sources=glob("pygad/C/src/*"),
        include_dirs=[
            "pygad/C/include",
            "/usr/include",
            gsl_include,
        ],
        extra_compile_args=extra_compile_args,
        libraries=libraries,
        extra_link_args=extra_link_args,
        library_dirs=[gsl_lib],
    )
    ext_modules = [ext_module]
else:
    print("Warning: GSL not found. pygad will be installed without the optional C extension.")
    print("         Install GSL and re-run pip if you want C acceleration for kernels and octrees.")

setup(
    name="pygadmpa",
    description="analysis module for Gadget",
    long_description="A light-weighted analysis module for galaxy \
        simulations performed by the SPH code Gadget.",
    author="Bernhard Roettgers",
    author_email="broett@mpa-garching.mpg.de",
    url="https://bitbucket.org/broett/pygad",
    include_package_data=True,
    packages=list(map(str, modules)),
    scripts=scripts,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    ext_modules=ext_modules,
)
