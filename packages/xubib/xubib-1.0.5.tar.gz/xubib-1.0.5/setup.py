from setuptools import setup

'''
    必要元素，name，version，description，packages等。
    常用元素，author，pymoudles,long_description,author_email,install_requires
'''
def markd(filename):
    with open(filename,encoding="utf-8") as rf:
        return rf.read()

#print (readme_file())
setup(
    name = "xubib",
    version = "1.0.5",
    packages = ["fb"],
    description = "this is my first test",
    author = "xushibo",
    author_email = "937207118@qq.com",
    #install_requires = ["bibtexparser"],#待测试
    install_requires = ["bibtexparser","mysqlclient" ],#待测试
    long_description = markd("README.rst")
    
    
)