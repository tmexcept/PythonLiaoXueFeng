'''
高阶函数除了可以接受函数作为参数外，还可以把函数作为结果值返回。
'''


def calc_num(*args):
    ax = 0
    for n in args:
        ax = ax + n
    return ax


print(calc_num(12, 23, 43))


# 但是，如果不需要立刻求和，而是在后面的代码中，根据需要再计算怎么办？可以不返回求和的结果，而是返回求和的函数：
def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax

    return sum


f = lazy_sum(23, 43, 545, 23)
# 当我们调用lazy_sum()时，返回的并不是求和结果，而是求和函数：
print(f)
# 调用函数f时，才真正计算求和的结果：
print(f())

'''
在这个例子中，我们在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力。

返回闭包时牢记的一点就是：返回函数不要引用任何循环变量，或者后续会发生变化的变量。
'''


def count():
    fs = []
    for i in range(1, 4):
        def f():
            return i * i

        fs.append(f)
    return fs


# 返回的函数引用了变量i，但它并非立刻执行。等到3个函数都返回时，它们所引用的变量i已经变成了3，因此最终结果为9。
f1, f2, f3 = count()
print(f1(), f2(), f3())


# 如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，无论该循环变量后续如何更改，已绑定到函数参数的值不变：
def count():
    def f(j):
        def g():
            return j * j

        return g

    fs = []
    for i in range(1, 4):
        fs.append(f(i))  # f(i)立刻被执行，因此i的当前值被传入f()
    return fs


f1, f2, f3 = count()
print(f1(), f2(), f3())

'''
# 返回函数 小结练习
'''


def createCounter():
    a = 0

    def counter():
        #a=a+1 是对a的再分配(reassign),需要指明nonlocal 而a[0]+=1 是对外部变量值的修改
        nonlocal a  #如果没有这一句运行的时候会报错，提示内部函数中的变量 a 未提前声明
        a += 1
        return a

    return counter


counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')


def createCounter2():
    a = [1]
    a[0] = 0

    def counter():
        a[0] += 1
        return a[0]

    return counter


counterA = createCounter2()
print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
counterB = createCounter2()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')


def createCounter3():
    def increase():
        n = 1
        while True:
            yield n
            n = n + 1

    f = increase()

    def counter():
        return next(f)

    return counter


counterA = createCounter3()
print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
counterB = createCounter3()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')
