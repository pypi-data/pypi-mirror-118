from setuptools import setup

'''
    必要元素，name，version，description，packages等。
    常用元素，author，pymoudles,long_description,author_email,install_requires
'''
def rf(filename):
    with open(filename,encoding="utf-8") as ff:
        return ff.read()
    



#print (readme_file())
setup(
    name = "bao",
    version = "1.0.3",
    description = "this is my first test",
    packages = ["bao"],
    py_modules = ["tool"],
    author = "xushibo",
    author_email = "937207118@qq.com",
    install_requires = ["bibtexparser"],#待测试
    long_description = rf("C:/Users/86135/Desktop/baobao/README.rst"),
    url="https://www.bilibili.com/"

)