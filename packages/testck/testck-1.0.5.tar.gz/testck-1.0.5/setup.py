from setuptools import setup

'''
    必要元素，name，version，description，packages等。
    常用元素，author，pymoudles,long_description,author_email,install_requires
'''



#print (readme_file())
setup(
    name = "testck",
    version = "1.0.5",
    packages = ["mhy"],
    description = "this is my first test",
    author = "chenkun",
    author_email = "qbei113043@163.com",
    install_requires = ["bibtexparser"],#待测试
    #install_requires = ["bibtexparser","mysqlclient" ],#待测试
    long_description = ("这是我们的尝试啊"),
    url="https://www.bilibili.com/"

)