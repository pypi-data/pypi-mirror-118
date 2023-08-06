from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='modelzoo_iitm',
    version = '0.0.29',
    description = 'Model Zoo by IIT Madras',
    py_modules = ["modelzoo_iitm", "UNet_zoo.model", "UNet_zoo.train", "UNetPP_zoo.model", "UNetPP_zoo.train", "StackGAN_zoo.model", "StackGAN_zoo.train1", "StackGAN_zoo.train2", "PointNet_zoo.model", "PointNet_zoo.train", "PSPNet_zoo.model", "PSPNet_zoo.train", "PSPNet_zoo.resnet", "Inpainting_zoo.loss", "Inpainting_zoo.model", "Inpainting_zoo.train", "Inpainting_zoo.utilities", "AdapAttnIC_zoo.model", "CharCNN_zoo.model", ],
    package_dir = {'': 'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "elasticdeform ~= 0.4.9",
        "sentence-transformers ~= 2.0.0",
        "PyPrind ~= 2.11.3"
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },
    url = "https://github.com/Vinayak-VG/ModelZoo_PyPi",
    author = "Vinayak-VG",
    author_email = "vinayakguptapokal@gmail.com",
    long_description = long_description,
    long_description_content_type = "text/markdown",
)