from setuptools import setup, find_packages

setup(
    name="wpgui",
    version="0.0.3",
    keywords=["pip", "testpypi"],
    description="test pip module, start a simple gui",
    long_description="test how to define pip module and upload to pypi, activate a simple gui",
    license="MIT",
    url="https://beyond.3dnest.cn/",  # your module home page, such as
    author="wp",  # your name
    author_email="wupengyu@3dnest.com",  # your email
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["PySimpleGUI", ]
)
