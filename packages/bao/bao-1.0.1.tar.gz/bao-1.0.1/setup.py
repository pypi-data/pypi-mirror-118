from setuptools import setup

'''
    必要元素，name，version，description，packages等。
    常用元素，author，pymoudles,long_description,author_email,install_requires
'''


#print (readme_file())
setup(
    name = "bao",
    version = "1.0.1",
    description = "this is my first test",
    packages = ["bao"],
    py_modules = ["tool"],
    author = "xushibo",
    author_email = "937207118@qq.com",
    #install_requires = ["bibtexparser"],#待测试
    long_description = "this is a long long long test",
    url="https://www.bilibili.com/"

)