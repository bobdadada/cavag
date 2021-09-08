
import numpy as np
from scipy import constants

__all__ = [
    'calculate_g', 'calculate_C1', 'calculate_eta_e',
    'calculate_eta_ext',
]

def calculate_g(V_mode, nu, gamma):
    """
    计算腔模-离子耦合系数g因子
    :param V_mode: 高斯驻波场模式体积
    :param nu: 光频率 = 光速/波长
    :param gamma: 驻波场对应频率能级跃迁的真空自发辐射速率
    :return: 耦合系数g
    """
    return np.sqrt((3*gamma*constants.pi*constants.c**3)/(2*V_mode*(2*np.pi*nu)**2))


def calculate_C1(g, kappa, gammat):
    """
    计算单原子耦合系数
    :param g: 耦合系数
    :param kappa: 腔泄漏损耗
    :param gammat: 总自发辐射速率
    :return: 耦合因子
    """
    return g**2/(kappa*gammat)


def calculate_eta_e(C1):
    """
    计算单原子发射几率
    :param C1: 耦合因子
    :return: 光子发射几率
    """
    return 2*C1/(2*C1+1)


def calculate_eta_ext(kappa, gammat):
    """
    计算腔耦合光子提取几率
    :param kappa: 腔泄露损耗
    :param gammat: 总自发辐射速率
    return: 腔耦合提取几率
    """
    return 2*kappa/(2*kappa+gammat)

