from setuptools import setup, find_packages

# Feel free to adapt these to your needs.
setup(
    name='tjts5901',
    packages=find_packages(),
    package_dir={"": "src"},
    include_package_data=True,
    license='MIT License',
    # use_scm_version=True,
    # setup_requires=['setuptools_scm'],
)
