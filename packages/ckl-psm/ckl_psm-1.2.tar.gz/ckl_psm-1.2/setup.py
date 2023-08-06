from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ckl_psm",
    version="1.2",
    author="snow0011",
    author_email="daslab@163.com",
    description="A password strength meter (PSM) with CKL_PCFG model",
    url="https://github.com/snow0011/CKL_PSM", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=[("",
        [
            "ckl_psm/resources/bpemodel.pickle",
            "ckl_psm/resources/dangerous_chunks.pickle",
            "ckl_psm/resources/monte_carlo_sample.pickle",
            "ckl_psm/resources/intermediate_results.pickle"
        ])],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)