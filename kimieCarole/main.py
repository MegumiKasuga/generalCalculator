from core.FunctionCalculator import FunctionCalculator

if __name__ == '__main__':

    # print('')

    # 计算器的定义和启动
    functionCalculator = FunctionCalculator()

    # 函数的加载
    functionCalculator.registerate_function('z=f(x,y2)=2x+y2+1')

    # 变量定义
    functionCalculator.define_variables('b=2.0')
    functionCalculator.define_variables('a=4.0')

    # 打印函数信息
    # functionCalculator.get_function('f').print()

    print('\nCalculating : 2^-114+5')

    # 计算demo
    print(functionCalculator.calculate('2^-114+5'))

    # print('')

    # 打印计算器内部信息
    # functionCalculator.print()



