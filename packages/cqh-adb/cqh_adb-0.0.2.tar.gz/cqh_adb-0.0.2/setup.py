import setuptools


name = 'cqh_adb'
long_description = """cdb
===================================

short for `cqh adb`
only work on windows


command list
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^





windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

设置env启动
-----------------------------------------

.. code-block::

    $env:PYTHONPATH=${PWD} ; python .\cdb\run.py logcat --value="com"

"""



version = "0.0.2"

setuptools.setup(
    name=name,  # Replace with your own username
    version=version,
    author="chenqinghe",
    author_email="1832866299@qq.com",
    description="cqh utils function",
    long_description=long_description,
    long_description_content_type='',
    url="https://github.com/chen19901225/cqh_util",
    packages=setuptools.find_packages(),
    install_requires=[
        "click"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            "cdb=cdb.run:cli",
        ],
    },
    python_requires='>=3.6',
    include_package_data=True
)