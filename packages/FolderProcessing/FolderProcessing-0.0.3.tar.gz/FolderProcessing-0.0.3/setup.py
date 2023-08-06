import setuptools

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="FolderProcessing", # 库名字
    version="0.0.3",#库版本
    author="PYmili",#作者名字
    author_email="mc2005wj@163.com",#联系邮件(可选)
    description="文件夹处理第三方库 The folder handles third-party libraries.",#描述这个库(可选)
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codechina.csdn.net/qq_53280175/folderprocessing",#代码存放地址(可选)
    packages=setuptools.find_packages(),
    classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          #'Programming Language :: Python',
          #'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',#使用版本
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )
