from setuptools import setup,find_packages


setup(
    name='dynautomate',
    version='0.1.1',
    description='parametric simulation workflow for LS-DYNA on hpc',
    author='Turner Jennings',
    author_email='turner.jennings@outlook.com',
    url='https://github.com/turnerjennings/dynautomate',
    license='MIT',
    packages=["src/dynautomate"],
    install_requires=[
        "numpy"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering"
    ]
)