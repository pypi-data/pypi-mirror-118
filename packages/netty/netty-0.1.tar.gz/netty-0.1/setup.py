import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="netty",                    
    version="0.1",                        
    author="Dexrey4 <https://github.com/dexrey4> and Enbyte Game Studios <https://github.com/enbyte>",                     # Full name of the author
    description="A simple python library for networking. Not extremely complex, but allows for simple game servers and chat rooms to be hosted.",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3',                
    include_package_data=True
)
