from setuptools import setup

'''
    必要元素，name，version，description，packages等。
    常用元素，author，pymoudles,long_description,author_email,install_requires
'''



#print (readme_file())
setup(
    name = "bitest",
    version = "1.0.0",
    description = "this is my first test",
    packages = ["bibib"],
    author = "xushibo",
    author_email = "937207118@qq.com",
    install_requires = ["bibtexparser","mysqlclient" ],#待测试
    long_description = ("这是我们的尝试啊"),
    url="https://www.bilibili.com/"

)