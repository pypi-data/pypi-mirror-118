from setuptools import setup, find_packages

setup(
    name="jismesh-raster",
    version="0.0.1",
    description="Generate raster from jismesh-based data. jismesh=Japan Standard Mesh",
    author="Kanahiro Iguchi",
    license="MIT",
    packages=find_packages(),
    install_requires=["jismesh", "pandas", "Pillow"],
    entry_points={
        "console_scripts": [
            "jismesh-raster=jismesh_raster.rasterize:main",
        ]
    }
)
