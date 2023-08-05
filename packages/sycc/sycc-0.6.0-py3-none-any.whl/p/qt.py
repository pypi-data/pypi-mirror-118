#from sys import path
#path.append('..')
#from p.__init__ import *
#from e.__init__ import *
#import platform
#os=platform.system()
#pai2='π'
#qt_font='\033[1;33m球体\033[0m\033[1;1m'
#公式
#'''
#S=4πR²
#V=4/3πR³
#'''
#V_314=round(4/3*3.14,6)
#print(V_314)
#def part_qt():
#    print('球体-β')
#    while True:
#        try:
#            r=eval(r=input('请输入半径'))
#            if r<=0:
#        	    print('你输入的数太小\n请重新选择'+qt_font+'模式重试')
#        	    switch(3)
#        	    break
#        except ZeroDivisionError:
#            print('除数不能为0')
#        except Exception:
#            print('半径:请输入有效数字')
#            print('半径:\033[6;31mError\033[0m\n')
#            print('请选择'+qt_font+'模式重试')
#            switch(2)
#            break
#        print('【'+qt_font+'】')
#        aboutpi()
#        if os=='Linux':
#            xxx=input('请输入(\033[1;32m1,2,3,4,5\033[0m\033[1;1m)中的一个数字:')
#        elif os=='Windows':
#            xxx=input('请输入1,2,3,4,5中的数字')
#        print('')
#        try:
#            xxx=int(xxx)
#        except ZeroDivisionError:
#            print('除数不能为0')
#        except (Exception,IOError,ValueError,TypeError,SyntaxError,EOFError,NameError,KeyboardInterrupt):
#            print('请输入指定范围的整数,不可以使用运算符')
#            switch(0.3)
#            break
#        try:
#        	if xxx>5 or xxx<=0:
#        		end1=sj.now()-start
#        		print('即将\033[10;31m退出\033[0m,','本次使用时间:',end1,'\n程序将在3s后关闭,谢谢使用')
#        		exitings(3)
#        		tc('谢谢使用')
#        	elif xxx==5:
#        		print('-'*40)
#        		switch(0.3)
#        		break
#        	elif xxx==1:
#        	    d=2*r
#        	    s=4*3.14*r**2