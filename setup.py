from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="awlf-astro",
    version="0.5.4",
    author="[Your Name]",
    author_email="[Your Email]",
    description="Physics-Aware Restoration for Astronomical Surveys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/[YourUsername]/AWLF-Astro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Image Processing",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "numba>=0.56.0",
        "scipy>=1.7.0",
        "opencv-python-headless>=4.5.0",
        "astropy>=5.0",
    ],
    extras_require={
        "dev": ["pytest", "matplotlib"],
    },
)
