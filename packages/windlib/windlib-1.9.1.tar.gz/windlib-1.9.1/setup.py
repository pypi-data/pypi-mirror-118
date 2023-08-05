try:
    from setuptools import setup
except ModuleNotFoundError:
    from distutils.core import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="windlib",
    version="1.9.1",
    author="SNWCreations",
    author_email="snwcreations@qq.com",
    description="A useful functions library for everyone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://gitee.com/SNWCreations/windlib",
    py_modules=['windlib'],
    project_urls={
        "Bug Tracker": "https://gitee.com/SNWCreations/windlib/issues",
    },
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "rarfile"
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
