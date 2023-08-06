import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qingtest",
    version="1.0.5",
    author="zhoujiahui",
    author_email="zhoujiahui@exiao.tech",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.qingflow.com",
    packages=setuptools.find_packages(),
    install_requires=['selenium==3.141.0','xlrd==1.2.0','XlsxWriter==1.3.7','requests==2.24.0','Appium-Python-Client==1.0.2','Pillow==8.0.1','openpyxl==3.0.5','arrow==0.17.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
