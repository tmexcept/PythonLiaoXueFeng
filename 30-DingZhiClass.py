'''
定制类

看到类似__slots__这种形如__xxx__的变量或者函数名就要注意，这些在Python中是有特殊用途的。

__slots__我们已经知道怎么用了，__len__()方法我们也知道是为了能让class作用于len()函数。
除此之外，Python的class中还有许多这样有特殊用途的函数，可以帮助我们定制类。
'''

'''
__str__
'''


class Student(object):
    def __init__(self, name):
        self.name = name


print(Student('Mic'))


# <__main__.Student object at 0x109afb190>
# 这样打印出来的实例，不但好看，而且容易看出实例内部重要的数据。
# 但是细心的朋友会发现直接敲变量不用print，打印出来的实例还是不好看
# 直接显示变量调用的不是__str__()，而是__repr__()，两者的区别是__str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，也就是说，__repr__()是为调试服务的。

class Student(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Student object (name:%s)' % self.name


print(Student('Mic'))
# __str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，也就是说，__repr__()是为调试服务的。

s = Student('Michael')
print(s)
print(s.__repr__())

'''
__iter__

如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，该方法返回一个迭代对象
然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。
'''


# 以斐波那契数列为例，写一个Fib类，可以作用于for循环：
class Fib(object):
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 100000:
            raise StopIteration()
        return self.a


for n in Fib():
    print(n)

'''
__getitem__

Fib实例虽然能作用于for循环，看起来和list有点像，但是，把它当成list来使用还是不行
比如，取第5个元素：
print(Fib()[5])
Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
TypeError: 'Fib' object does not support indexing

要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
'''


class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a


f = Fib()
print(f[0])
print(f[10])
print(f[20])
print(f[30])
print(f[40])
print(f[50])

# 但是list有个神奇的切片方法：
list(range(100))[5:10]
[5, 6, 7, 8, 9]


# Fib却报错
# 原因是__getitem__()传入的参数可能是一个int，也可能是一个切片对象slice，所以要做判断：
class Fib(object):
    """docstring for Fib"""

    def __getitem__(self, n):
        if isinstance(n, int):
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L


f = Fib()
print(f[0:10])
print(f[:20])
# 但是没有对step参数作处理：
f[:10:2]
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
# 也没有对负数作处理，所以，要正确实现一个__getitem__()还是有很多工作要做的。
# 此外，如果把对象看成dict，__getitem__()的参数也可能是一个可以作key的object，例如str。
# 与之对应的是__setitem__()方法，把对象视作list或dict来对集合赋值。最后，还有一个__delitem__()方法，用于删除某个元素。
# 总之，通过上面的方法，我们自己定义的类表现得和Python自带的list、tuple、dict没什么区别，这完全归功于动态语言的“鸭子类型”，不需要强制继承某个接口

'''
__getattr__

正常情况下，当我们调用类的方法或属性时，如果不存在，就会报错。
'''


class Student(object):
    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr == 'score':
            return 99
        return attr


# 调用name属性，没问题，但是，调用不存在的score属性，就有问题了：
s = Student()
print(s.name)
print(s.score)
print(s.asd)


# AttributeError: 'Student' object has no attribute 'score'
# 错误信息很清楚地告诉我们，没有找到score这个attribute。


# 要避免这个错误，除了可以加上一个score属性外，Python还有另一个机制，那就是写一个__getattr__()方法，动态返回一个属性。修改如下：
class Student(object):

    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr == 'score':
            return 99


# 当调用不存在的属性时，比如score，Python解释器会试图调用__getattr__(self, 'score')来尝试获得属性，这样，我们就有机会返回score的值：
s = Student()
s.name
'Michael'
s.score
99


# 返回函数也是完全可以的：
class Student(object):
    def __getattr__(self, attr):
        if attr == 'age':
            return lambda: 25


# 只是调用方式要变为：
s.age()
25


# 注意，只有在没有找到属性的情况下，才调用__getattr__，已有的属性，比如name，不会在__getattr__中查找。
# 此外，注意到任意调用如s.abc都会返回None，这是因为我们定义的__getattr__默认返回就是None。要让class只响应特定的几个属性，我们就要按照约定，抛出AttributeError的错误：

class Student(object):

    def __getattr__(self, attr):
        if attr == 'age':
            return lambda: 25
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)


# 这实际上可以把一个类的所有属性和方法调用全部动态化处理了，不需要任何特殊手段。
# 这种完全动态调用的特性有什么实际作用呢？作用就是，可以针对完全动态的情况作调用。
# 举个例子：
# 现在很多网站都搞REST API，比如新浪微博、豆瓣啥的，调用API的URL类似：
# http://api.server/user/friends
# http://api.server/user/timeline/list
# 如果要写SDK，给每个URL对应的API都写一个方法，那得累死，而且，API一旦改动，SDK也要改。

# 利用完全动态的__getattr__，我们可以写出一个链式调用：
# 链式调用
class Chain(object):
    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    __repr__ = __str__


print(Chain().status.user.timeline.list)
# '/status/user/timeline/list'
# 这样，无论API怎么变，SDK都可以根据URL实现完全动态的调用，而且，不随API的增加而改变！
# 还有些REST API会把参数放到URL中，比如GitHub的API：
# GET /users/:user/repos
# 调用时，需要把:user替换为实际用户名。如果我们能写出这样的链式调用：
Chain().users('michael').repos
# 就可以非常方便地调用API了【在文末有完整实例】
'''
__call__

一个对象实例可以有自己的属性和方法，当我们调用实例方法时，我们用instance.method()来调用。
能不能直接在实例本身上调用呢？在Python中，答案是肯定的
'''


# 任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用。
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        print('My name is %s.' % self.name)


s = Student('Michael')
s()
Student('jue')()
# __call__()还可以定义参数。对实例进行直接调用就好比对一个函数进行调用一样，所以你完全可以把对象看成函数，把函数看成对象，因为这两者之间本来就没啥根本的区别。
# 如果你把对象看成函数，那么函数本身其实也可以在运行期动态创建出来，因为类的实例都是运行期创建出来的，这么一来，我们就模糊了对象和函数的界限。

# 怎么判断一个变量是对象还是函数呢？
# 其实，更多的时候，我们需要判断一个对象是否能被调用，能被调用的对象就是一个Callable对象
# 比如函数和我们上面定义的带有__call__()的类实例：
print(callable(Student('')))
True
print(callable(max))
True
print(callable([1, 2, 3]))
False
print(callable(None))
False
print(callable('str'))
False
# 通过callable()函数，我们就可以判断一个对象是否是“可调用”对象


# =============================================
# 完全动态调用特性：
# 把一个类的所有属性和方法调用全部动态化处理

# __call__(): 用于实例自身的调用，达到()调用的效果
# 即可以把此类的对象当作函数来使用，相当于重载了括号运算符
# __getattr__(): 当调用不存在的属性时调用此方法来尝试获得属性
class Chain(object):
    # def __init__(self, path=''):    # 默认路径参数path为空
    #     self._path = path

    # def __getattr__(self, path):
    #     print('call __getattr__(%s)' % path)
    #     return Chain('%s/%s' % (self._path, path))

    def __str__(self):
        return self._path

    def __call__(self, param):
        print('cal __call__(%s)' % param)
        return Chain('%s/%s' % (self._path, param))

    def __init__(self, path='', user=None):
        self._path = path
        self._user = user

    def __getattr__(self, path):
        if path == 'users':
            return Chain('%s/%s/:%s' % (self._path, path, self._user),user=self._user)
        return Chain('%s/%s' % (self._path, path),user=self._user)

    __repr__ = __str__


# /status/user/timeline/list
# Chain().status.user.timeline.list调用分析
# 首先执行Chain()返回一个实例对象C1(path = '')，
# 通过实例对象C1来获取status属性，因为C1中不存在status属性，所以就会调用
# __getattr__()来尝试获取status属性，接着通过__getattr__()方法返回
# 带参数status的实例对象C2(path = '/status')，然后通过实例对象C2来获取user属性，
# C2中不存在user属性，接着调用__getattr__()方法返回带参数user
# 的实例对象C3(path = '/status/user')，然后通过实例对象C3来获取timeline属性，
# 因C3不存在timeline属性，故调用__getattr__()方法返回带参数timeline
# 的实例对象C4(path = '/status/user/timeline')，通过实例对象C4来获取list属性，
# 又因C4中不存在list属性，调用__getattr__()方法返回带参数list
# 的实例对象C5(path = '/status/user/timeline/list')，
# 最后通过调用__str__()方法来打印实例对象C5，即返回/status/user/timeline/list
# 具体参考见下面的测试结果
print(Chain().status.user.timeline.list)
print('--------------------------------------')
print(Chain(user='Bob').big.bad.pop.users.bin)
# /big/bad/pop/users/:Bob/bin       这个不会调用__call__方法
print(Chain(user='Bob').big.bad('haha').users.bin)
# /big/bad/haha/pop/users/:None/bin  这个会调用__call__方法

# GET /users/:user/repos
# :user替换为实际用户名
# /users/Lollipop/repos
# Chain().users('Lollipop').repos 调用分析
# 首先执行Chain()返回一个实例对象Q1(path = '')，
# 通过实例对象Q1来获取users属性，因为Q1中不存在users属性，
# 所以就会调用__getattr__()方法尝试获取users属性，接着通过
# __getattr__()方法返回带参数users的实例对象Q2(path = '/users')，
# 然后因为通过()直接调用实例对象Q2，并带参数'Lollipop'，故会调用
# __call__()方法，返回了带参数Lollipop的实例对象Q3(path = '/users/Lollipop')，
# 接着通过实例对象Q3来获取repos属性，又因Q3中不存在repos属性，即会调用
# __getattr__()方法返回带参数repos的实例对象Q4(path = '/users/Lollipop/repos')
# 最后通过调用__str__()方法来打印实例对象Q4，即返回/users/Lollipop/repos
# 具体参考见下面的测试结果
print(Chain().users('Lollipop').repos)

'''
# log analysis
call __getattr__(status)
call __getattr__(user)
call __getattr__(timeline)
call __getattr__(list)
/status/user/timeline/list
--------------------------------------
call __getattr__(users)
cal __call__(Lollipop)
call __getattr__(repos)
/users/ollipop/repos
'''
# 疑惑
# １．为什么实例对象会获取status属性？
# ２. 明明没有循环语句，为什么能够持续地返回？
# 解释：
# １．因为'.'这个符号，代表的就是“实例.属性”这一绑定关系，在前几章老师已经教过了。
# ２．Chain().status.user.timeline.list这个式子，代表的就是chain（）的status属性的user属性的timelin属性的list属性，
# 这种俄罗斯套娃的即视感有没有让大家想起函数式编程的reduce（）方法？就是这样，通过层层剥离，就能够产生持续的返回效果。

