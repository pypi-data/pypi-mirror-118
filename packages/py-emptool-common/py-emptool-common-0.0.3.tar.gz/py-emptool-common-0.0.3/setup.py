from setuptools import setup, find_packages

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name='py-emptool-common',
    version='0.0.3',

    description='Common Emptool functions',
    long_description=long_description,
    long_description_content_type="text/markdown",

    url='https://github.com/ongzhixian/py-emptool-common',
    
    author='ONG ZHI XIAN',
    author_email='zhixian@hotmail.com',

    #packages=['funniest'],
    package_dir={"": "emptool"},
    packages=find_packages(where="emptool"),

    install_requires=[
        # "aws-cdk.core==1.118.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",
        
        "Intended Audience :: Developers",
        
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        
        # "Topic :: Software Development :: Helpers",
        "Topic :: Utilities",
        
        # "Typing :: Typed",
    ],

    license='MIT'
)