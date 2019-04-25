''''''
'''
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False用来解决不能使用汉字问题，需要导入matplotlib
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
import math

x=np.arange(0.05,3,0.05)

#设置X坐标轴
y1=[5 for i in x]
plt.plot(x,y1,linewidth=2,label=u'常函数：y=5')

#常函数
y2=[2*i+1 for i in x]
plt.plot(x,y2,linewidth=2,label=u'一次函数：y=2x+1')

#二次函数，在$内的内容能正确显示x^2
y3=[1.5*i*i-3*i+1 for i in x]
plt.plot(x,y3,linewidth=2,label=u'二次函数：y=1.5$x^2$-3x+1')

#幂函数，math,pow(x,y)  x是底数 y是指数
y4=[math.pow(i,2) for i in x]
plt.plot(x,y4,linewidth=2,label=u'幂函数：y=$x^2$')

#指数函数
y5=[math.pow(2,i) for i in x]
plt.plot(x,y5,linewidth=2,label=u'指数函数：y=$2^x$')

#对数函数，math.log(x,y) y是可以设置的底数
y6=[math.log(i,2) for i in x]
plt.plot(x,y6,linewidth=2,label=u'对数函数：y=logx2(x)')

#-4pi到4pi之间产生一百个等差值
x1=np.linspace(-4*np.pi,4*np.pi,100)
y7=[np.sin(i) for i in x1]
y8=[np.cos(i) for i in x1]
plt.plot(x1,y7,label='y=sin(x)',c='g',linewidth=2)
plt.plot(x1,y8,label='y=cos(x)',c='r',linewidth=2)

#突出某条具体的线
# plt.plot([1,1],[-3],5,'--',color='#999999',linestyle=2)
#plt.grid(True)是否显示网格线
plt.legend(loc='lower right')
plt.grid(True)
plt.show()