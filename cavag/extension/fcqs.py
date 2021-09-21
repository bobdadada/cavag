
import numpy as np
from scipy import constants as C

__all__ = [
    'calculate_mu', 'calculate_emax',
    'calculate_g', 'calculate_c1', 'calculate_eta_e',
    'calculate_eta_ext',
]


def calculate_mu(nu, gamma):
    """
    计算电偶极跃迁的电偶极距

    此公式为导出公式，并不是电偶极矩的定义式。它计算了按照一定自发辐射速率
    发射的光子所对应的电偶极距。

    :param nu: 跃迁频率
    :param gamma: 对应频率能级跃迁的真空自发辐射速率
    :return: 电偶极距
    """
    return np.sqrt(3*C.pi*C.epsilon_0*C.hbar*C.c**3*gamma/(2*C.pi*nu)**3)


def calculate_emax(v_mode, nu):
    """
    计算腔膜峰值的电场强度

    如果我们知道腔膜模式体积，则我们可以利用此公式计算单光子电场强度峰值。

    :param v_mode: 驻波场模式体积
    :param nu: 驻波场频率
    :return: 单光子驻波电场峰值
    """
    return np.sqrt(C.h*nu/(2*C.epsilon_0*v_mode))


def calculate_g(mu, e):
    """
    计算腔模-粒子能级耦合系数g因子

    此耦合系数g并不关心跃迁频率是否与电场频率相等。当频率不相等时，实际的
    耦合强度需要额外乘以一个与频率有关的系数。

    :param mu: 对应跃迁的电偶极矩
    :param e: 粒子所在位置的电场强度
    :return: 耦合系数
    """
    return mu*e/C.hbar


def calculate_c1(g, kappa, gammat):
    """
    计算单原子耦合系数

    公式中kappa用腔透射曲线半高半宽定义，部分文献中使用半高全宽定义，注意区别。
    此C1因子具体定义可以参考文献：
    - Guoqiang Cui etc.; Quantum efficiency of single-photon sources in the 
        cavity-QED strong-coupling regime

    :param g: 耦合系数
    :param kappa: 腔泄漏速率
    :param gammat: 总自发辐射速率
    :return: 耦合因子
    """
    return g**2/(kappa*gammat)


def calculate_eta_e(c1):
    """
    计算单原子发射几率

    此C1因子具体定义可以参考文献：
    - Guoqiang Cui etc.; Quantum efficiency of single-photon sources in the 
        cavity-QED strong-coupling regime
    部分文献定义类似的耦合因子，注意区别。

    :param c1: 耦合因子
    :return: 光子发射几率
    """
    return 2*c1/(2*c1+1)


def calculate_eta_ext(kappa, gammat):
    """
    计算腔耦合光子提取几率

    公式中kappa用腔透射曲线半高半宽定义，部分文献中使用半高全宽定义，注意区别。

    :param kappa: 腔泄露速率
    :param gammat: 总自发辐射速率
    :return: 腔耦合提取几率
    """
    return 2*kappa/(2*kappa+gammat)

def calculate_eta_trans(rtl, rtr, lc, direction='both'):
    """
    计算腔中光子等效透射几率

    假设腔内含有某个模式的单光子，求等效透射几率。

    :param rtl: (r, t) 左边介质膜的(反射率，透射率)
    :param rtr: (r, t) 右边介质膜的(反射率，透射率)
    :param lc: 腔内损耗
    :param direction: 透射方向，可为left、right、both，默认为both
    """
    rl0, tl0 = rtl
    rr0, tr0 = rtr

    # 由于腔内损耗在一个来回中要经历两次，可以将腔内损耗等效地添加到左右介质膜中
    rl, rr = rl0*(1-lc), rr0*(1-lc)

    pass

    # 适当的缓存以减少计算量
    s = (1-lc)/(1-rl*rr)/2   

    # 计算等效透射率
    if direction == 'left':
        return tl0*(1-rl)*(1+rr)*s
    elif direction == 'right':
        return tr0*(1-rr)*(1+rl)*s
    else:
        return tr0*(1-lc)*(1-rr)*(1+rl)/(1-rl*rr)/2

