import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ml-platform-client",
    version="0.4.8",
    author="JeremyXin",
    author_email="chengjiexin@emotibot.com",
    description="emotibot ml platform client for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        "flask-restful",
        "minio",
        "pymysql",
        "psutil",
        "mlp_tracking>=0.0.3",
        "sqlalchemy==1.4.7",
        "pymysql==0.9.3",
        "pymssql==2.1.5",
        "psycopg2-binary==2.9.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
