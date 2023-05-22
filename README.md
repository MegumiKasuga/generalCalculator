# generalCalculator
- 一个通用函数计算器

#### How to use
`
  from core.FunctionCalculator import FunctionCalculator # 导入库

  # 计算器的定义和启动
  functionCalculator = FunctionCalculator()

  # 函数加载
  functionCalculator.registerate_function('z=f(x,y2)=2x+y2+1')

  # 变量定义
  functionCalculator.define_variables('b=c=2.0')
  functionCalculator.define_variables('a=4.0')

  # 打印函数信息
  # functionCalculator.get_function('f').print()

  # 计算demo
  print(functionCalculator.calculate('2^-114+5'))

  # 打印计算器内部信息
  functionCalculator.print()
`
