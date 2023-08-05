import setuptools

require_twill = ['requests>=2.25,<3']
setuptools.setup(
    name="lichvansu",
    version="2021.8.9",
    author="@trumxuquang",
    author_email="trumxuquang@gmail.com",
    description="https://vnhass.blogspot.com/",
    long_description="https://vnhass.blogspot.com/",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=require_twill,
)