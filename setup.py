import setuptools


setuptools.setup(
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": [f"consult = consult:run_consult"]},
    install_requires=["Click>=7.0"],
)
