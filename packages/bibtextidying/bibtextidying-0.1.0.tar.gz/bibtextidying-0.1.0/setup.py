from setuptools import setup

'''
    必要元素，name，version，description，packages等。
    常用元素，author，pymoudles,long_description,author_email,install_requires
'''
 


#print (readme_file())
setup(
    name = "bibtextidying",
    version = "0.1.0",
    packages = ["finalbib"],
    description = "Help to use bib_file more easily",
    author = "Jian Ding and ShiBo Xu and Kun Chen",
    author_email = "937207118@qq.com",
    install_requires = ["bibtexparser","mysqlclient" ],
    long_description = open('README.md',"r").read(),
    long_description_content_type ="text/markdown",
    license="MIT"
)