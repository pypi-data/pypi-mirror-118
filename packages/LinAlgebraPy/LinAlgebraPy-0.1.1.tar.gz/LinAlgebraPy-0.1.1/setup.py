from setuptools import _install_setup_requires, find_packages, setup

setup(
    name='LinAlgebraPy',
    packages=find_packages(),
    version='0.1.1',
    description='Linear Algebra Package',
    author='Rami El Dahouk',
    license='MIT',
    install_requires=["sympy","numpy"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='test',
)