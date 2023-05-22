# generalCalculator
- 一个通用函数计算器
- 输入一个函数、代数式进行计算，获得一个返回值

#### How to use
  
  ##### 导入库
  `from core.FunctionCalculator import FunctionCalculator`

  ##### 计算器的定义和启动
  `functionCalculator = FunctionCalculator()`
  
  该句定义一个函数计算器

  ##### 函数加载
  `functionCalculator.registerate_function('z=f(x,y2)=2x+y2+1')`
  
  该句向函数计算器中注册一个函数。注册的函数可以被直接调用。左侧定义的因变量是可以连等的

  ##### 变量定义
  `functionCalculator.define_variables('b=c=2.0')`
  
  变量的定义是允许连等的
  
  `functionCalculator.define_variables('a=4.0')`

  ##### 打印函数信息
  `functionCalculator.get_function('f').print()`
  
  该句将打印函数计算器中指定函数的信息

  ##### 计算
  `print(functionCalculator.calculate('2^-114+5'))`
  
  该句(`calculate(expression)方法`)用于解算给定的计算式

  ##### 打印计算器内部信息
  `functionCalculator.print()`
  
  打印计算器内部信息
  
  ##### 严格模式
  `functionCalculator.strict_mode(bool)`
  
  启停计算器严格模式
  
  严格模式下，用户输入未定义的变量值将被视为非法。而非严格模式下，将会将未定义的变量转换为设定的缺省值
  
  通过`functionCalculator.set_default_var(number)`来调整缺省值，默认为0.0
