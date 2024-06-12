import numpy as np
import math
import matplotlib.pyplot as plt
import numpy as np

# 曲面用一个函数来表示,即传入坐标,当在曲目上时返回0 (也许: 内部正数,外部负数)
# 传入曲面上点的坐标,返回曲面的法方向和折射率
# 光线用函数来表示,函数接受参数t,返回在t时刻的位置(不遇到界面时)

# 再有一个程序负责接受这两个函数加一组光线来模拟并渲染.
# ---------------------------------

debug =True

def draw_line(pos1 , pos2 , color= 'blue' , d = 0.5):
    plt.plot([pos1[0] , pos2[0]] ,[pos1[1] , pos2[1]] , color= color , linewidth = d)
    # plt.show()

def make_light(begin_pos , direction):
    return lambda t : (begin_pos[0] + t*direction[0] , begin_pos[1] + t*direction[1])

def refraction(f , s_n ,t):
    def theta(direction):
        return np.arctan2(direction[1] , direction[0])
    def direction(theta):
        return np.array([np.cos(theta) , np.sin(theta)])
    a , k = s_n(f(t))
    direction_1 = np.array(f(t-1)) - np.array(f(t))
    direction_2 = np.array(a)
    theta_1 = theta(direction_1)
    theta_2 = theta(direction_2)
    if debug:
        p = np.array(f(t))
        draw_line(p-0.01*direction(theta_2) , p+0.01*direction(theta_2) , d=1 , color='red')
        draw_line(p-0.001*direction(theta_1) , p+0.01*direction(theta_1) , d=1 , color='green')

    if np.dot(direction_1 , direction_2)>0:
        theta_3 =np.arcsin( np.sin(theta_1-theta_2)/k ) + np.pi + theta_2
    else :
        tmp = np.sin(theta_1-theta_2)*k
        if tmp>1 or tmp<-1 :
            return None
        theta_3 = - np.arcsin( tmp ) + theta_2
    return make_light(f(t) , direction(theta_3))

def make_is_out( size ):
    '''生成函数判断是否超出边界'''
    def is_out(pos):
        if (pos[0]<size[0]) or (pos[0] > size[1]) or (pos[1]<size[2]) or (pos[1] > size[3]) :
            return -1
        else:
            return 1
    return is_out
def solve_f(f , a , b , d = 1e-14):
    if f(a)<0:
        a,b = b,a
    while(abs(a-b) > d):
        c = (a+b)/2
        if f(c) > 0:
            a = c
        else:
            b = c
    return (a+b)/2
def solve2_f(g , a , b ):
    if g(a)<0 :
        f = lambda x: -g(x)
    else :
        f = lambda x: g(x)
    step = 0.1
    t = a
    while(t<b):
        if f(t)<0 :
            break
        t = t + step
    else:
        step = 0.01
        t = a
        while(t<b):
            if f(t)<0 :
                break
            t = t + step
        else:
            step = 0.001
            t = a
            while(t<b):
                if f(t)<0 :
                    break
                t = t + step
            else:
                return b
    return solve_f(f , t-step , t)
def find_t(f , s , is_out ):
    '''寻找下一次经过界面的时间'''
    t0 = 0
    while(is_out(f(t0)) > 0):
        t0 = t0 + 2
    t0 = solve_f(lambda t : is_out(f(t)) , t0-2 , t0 , 0.1)
    t1 = solve2_f(lambda t: s(f(t)) , 0 , t0)
    if t1>t0-1e-6:
        return t1+0.1
    else :
        return t1+1e-6


def simulate(s , s_n , lights , size = (-2,2,-2,2)):
    is_out = make_is_out(size)
    for f in lights:
        i=0
        while(i<4):
            t = find_t(f , s , is_out)
            draw_line(f(0) , f(t))
            if is_out(f(t)) < 0:
                break
            f = refraction(f , s_n , t)
            if f==None:
                break
            # i = i+1
    plt.axis('equal')
    plt.show()

def s(pos):
    return 1 - (pos[0]*pos[0] + pos[1]*pos[1])
def n(pos):
    return (pos,3)

def s2(pos):
    if pos[0] <0:
        return 10.1**2 - (pos[0]-10)**2 - pos[1]**2
    else :
        return 10.1**2 - (pos[0]+10)**2 - pos[1]**2
def n2(pos):
    if pos[0] <0:
        return (pos[0]-10 , pos[1]),3
    else:
        return (pos[0]+10 , pos[1]),3
def s3(pos):
    if pos[0] >0:
        return 1
    else :
        return -1
def n3(pos):
    return (-1, pos[1]),3

lights = [make_light((-2,i) , (1,0)) for i in np.linspace(-0.9 , 0.9 , 50)]

simulate(s, n ,lights ,(-2,2,-2,2))
simulate(s2, n2 ,lights , (-2,4,-2,2))
simulate(s3, n3 , lights , (-2,2,-2,2)) 
