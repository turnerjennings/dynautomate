from setuptools import setup,find_packages


setup(
    name='dynautomate',
    version='0.1.0.dev0',
    description='parametric simulation workflow for LS-DYNA on hpc',
    author='Turner Jennings',
    author_email='turner.jennings@outlook.com',
    url='https://github.com/turnerjennings/dynautomate',
    license='MIT',
    packages=find_packages(),
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