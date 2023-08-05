from distutils.core import setup

setup(
    name='baizhanSuperMath0826',        # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，测试哦',  # 描述
    author = 'xsy' , # 作者
    author_email='gaoqi110@163.com',
    py_modules=['baizhanSuperMath0826.demo1','baizhanSuperMath0826.demo2']  # 要发布的模块
)