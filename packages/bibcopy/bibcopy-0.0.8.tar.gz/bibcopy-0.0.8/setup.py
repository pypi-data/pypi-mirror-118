from setuptools import setup

'''
    必要元素，name，version，description，packages等。
    常用元素，author，pymoudles,long_description,author_email,install_requires
'''
 


#print (readme_file())
setup(
    name = "bibcopy",
    version = "0.0.8",
    packages = ["fb"],
    description = "fix some bugs in bibcopy",
    author = "chenkun",
    author_email = "qbei113043@163.com",
    #install_requires = ["bibtexparser"],#待测试
    install_requires = ["bibtexparser","mysqlclient" ],#待测试
    long_description = open('README.md',"r").read(),
    long_description_content_type ="text/markdown"
)