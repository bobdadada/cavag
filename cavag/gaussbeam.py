import numpy as np
from scipy import constants
from scipy import special
from .misc import Wavelength

__all__ = [
    'NormalizedHermiteGaussBeam1D', 'HermiteGaussBeam1D',
    'NormalizedGaussBeam1D', 'GaussBeam1D',
    'NormalizedHermiteGaussBeam', 'HermiteGaussBeam',
    'NormalizedGaussBeam', 'GaussBeam',
    'NormalizedAxisymmetricHermiteGaussBeam', 'AxisymmetricHermiteGaussBeam',
    'NormalizedAxisymmetricGaussBeam', 'AxisymmetricGaussBeam',
    'local2remote', 'remote2local', 'convert_through_mirror', 'convert_through_lens'
]


class NormalizedHermiteGaussBeam1D(Wavelength):
    name = 'NormalizedHermiteGaussBeam1D'

    # 波长, 束腰位置, 束腰半径, 模式数
    modifiable_properties = ('wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='NormalizedHermiteGaussBeam1D', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(
            NormalizedHermiteGaussBeam1D.modifiable_properties)

        for prop in NormalizedHermiteGaussBeam1D.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def c(self):
        """归一化因子"""
        def v_f():
            omega0 = self.omega0
            m = self.m
            return (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        return self.get_property('c', v_f)

    @property
    def p0(self):
        """束腰位置"""
        return self.get_property('p0')

    @property
    def omega0(self):
        """束腰半径"""
        return self.get_property('omega0')

    @property
    def theta(self):
        """半发散角"""
        return self.get_property('theta', lambda: np.sqrt(2*self.m+1)*np.arctan(self.wavelength/(constants.pi*self.omega0)))

    @property
    def m(self) -> int:
        """光的模式数"""
        return self.get_property('m')

    @property
    def z0(self):
        """瑞利长度"""
        return self.get_property('z0', lambda:  constants.pi * (self.omega0) ** 2 / self.wavelength)

    @property
    def hm(self):
        """Hermite多项式"""
        return self.get_property('hm', lambda:  special.hermite(self.m))

    def A_f(self, z):
        """振幅函数"""
        z0, p0 = self.z0, self.p0
        return 1/(1+((z-p0)/z0)**2)**(1/4)

    def omega_f(self, z):
        """模场半径函数"""
        omega0, z0, p0 = self.omega0, self.z0, self.p0
        return omega0*np.sqrt(1 + ((z-p0)/z0)**2)

    def R_f(self, z):
        """波前曲率半径函数"""
        z0, p0 = self.z0, self.p0
        return (z-p0)*(1+(z0/(z-p0))**2)

    def phi_f(self, z):
        """phi相位函数"""
        z0, p0 = self.z0, self.p0
        return np.arctan((z-p0)/z0)

    def psi_f(self, z, x):
        """HG函数"""
        hm = self.hm
        omega = self.omega_f(z)
        xi = np.sqrt(2)*x/omega

        return hm(xi)*np.exp(-xi**2/2)

    def u_f(self, z, x):
        """强度函数"""
        c = self.c
        A = self.A_f(z)
        psi = self.psi_f(z, x)
        phi = self.phi_f(z)
        k = self.k
        R = self.R_f(z)
        m = self.m

        ampl = c*A*psi
        phase = -k/(2*R)*x**2+(m+1/2)*phi

        return ampl, phase


class HermiteGaussBeam1D(NormalizedHermiteGaussBeam1D):
    name = 'HermiteGaussBeam1D'

    # 振幅, 波长, 束腰位置, 束腰半径, 模式数
    modifiable_properties = ('A0', 'wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='HermiteGaussBeam1D', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required('A0')
        self.property_set['A0'] = kwargs.get('A0', None)

    @property
    def A0(self):
        """振幅"""
        return self.get_property('A0')

    def A_f(self, z):
        """振幅函数"""
        A0 = self.A0
        A = super().A_f(z)
        print(A)
        return A0*A


class NormalizedGaussBeam1D(NormalizedHermiteGaussBeam1D):
    name = 'NormalizedGaussBeam1D'

    modifiable_properties = ('wavelength', 'omega0', 'p0')

    def __init__(self, name='NormalizedGaussBeam1D', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


class GaussBeam1D(HermiteGaussBeam1D):
    name = 'GaussBeam1D'

    modifiable_properties = ('A0', 'wavelength', 'p0', 'omega0')

    def __init__(self, name='GaussBeam1D', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


class NormalizedHermiteGaussBeam(Wavelength):
    name = 'NormalizedHermiteGaussBeam'

    # 波长, 束腰位置, x方向束腰半径, y方向束腰半径, x方向束腰位置, x方向模式数, y方向模式数
    modifiable_properties = (
        'wavelength', 'p0', 'omega0x', 'omega0y', 'mx', 'my')

    def __init__(self, name='NormalizedHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(
            NormalizedHermiteGaussBeam.modifiable_properties)

        for prop in NormalizedHermiteGaussBeam.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

        __kwarg_beams = ({
            'wavelength': kwargs.get('wavelength', None),
            'p0': kwargs.get('p0', None),
            'omega0': kwargs.get('omega0x', None),
            'm': kwargs.get('mx', None),
        }, {
            'wavelength': kwargs.get('wavelength', None),
            'p0': kwargs.get('p0', None),
            'omega0': kwargs.get('omega0y', None),
            'm': kwargs.get('my', None),
        })

        self.__beams = (
            NormalizedHermiteGaussBeam1D(
                name='x-direction', **(__kwarg_beams[0])),
            NormalizedHermiteGaussBeam1D(
                namm='y-direction', **(__kwarg_beams[1])),
        )

    def postprocess_properties(self, **propdict):
        xkw, ykw = {}, {}
        for k, v in propdict.items():
            if k.endswith('x'):
                xkw[k[:-1]] = v
            elif k.endswith('y'):
                ykw[k[:-1]] = v
            else:
                xkw[k] = ykw[k] = v

        if xkw:
            self.__beams[0].change_params(**xkw)
        if ykw:
            self.__beams[1].change_params(**ykw)

    @property
    def cx(self):
        """x方向归一化因子"""
        return self.get_property('cx', lambda: self.__beams[0].c)

    @property
    def cy(self):
        """y方向归一化因子"""
        return self.get_property('cy', lambda: self.__beams[1].c)

    @property
    def c(self):
        """总归一化因子"""
        return self.get_property('c', lambda: self.cx*self.cy)

    @property
    def p0(self):
        """束腰位置"""
        return self.get_property('p0')

    @property
    def omega0x(self):
        """x方向束腰半径"""
        return self.get_property('omega0x')

    @property
    def omega0y(self):
        """y方向束腰半径"""
        return self.get_property('omega0y')

    @property
    def thetax(self):
        """x方向半发散角"""
        return self.get_property('thetax', lambda: self.__beams[0].theta)

    @property
    def thetay(self):
        """y方向半发散角"""
        return self.get_property('thetay', lambda: self.__beams[1].theta)

    @property
    def mx(self) -> int:
        """x方向光的模式数"""
        return self.get_property('mx')

    @property
    def my(self) -> int:
        """y方向光的模式数"""
        return self.get_property('my')

    @property
    def z0x(self):
        """x方向瑞利长度"""
        return self.get_property('z0x', lambda: self.__beams[0].z0)

    @property
    def z0y(self):
        """y方向瑞利长度"""
        return self.get_property('z0y', lambda: self.__beams[1].z0)

    @property
    def hmx(self):
        """x方向Hermite多项式"""
        return self.get_property('hmx', lambda: self.__beams[0].hm)

    @property
    def hmy(self):
        """y方向Hermite多项式"""
        return self.get_property('hmy', lambda: self.__beams[1].hm)

    def A_f(self, z):
        """振幅函数"""
        return self.__beams[0].A_f(z)*self.__beams[1].A_f(z)

    def omegax_f(self, z):
        """x方向模场半径函数"""
        return self.__beams[0].omega_f(z)

    def omegay_f(self, z):
        """y方向模场半径函数"""
        return self.__beams[1].omega_f(z)

    def Rx_f(self, z):
        """x方向波前曲率半径函数"""
        return self.__beams[0].R_f(z)

    def Ry_f(self, z):
        """y方向波前曲率半径函数"""
        return self.__beams[1].R_f(z)

    def phix_f(self, z):
        """x方向phi相位函数"""
        return self.__beams[0].phi_f(z)

    def phiy_f(self, z):
        """y方向phi相位函数"""
        return self.__beams[1].phi_f(z)

    def psix_f(self, z, x):
        """x方向HG函数"""
        return self.__beams[0].psi_f(z, x)

    def psiy_f(self, z, y):
        """y方向HG函数"""
        return self.__beams[1].psi_f(z, y)

    def u_f(self, z, x, y):
        """强度函数"""
        amplx, phasex = self.__beams[0].u_f(z, x)
        amply, phasey = self.__beams[1].u_f(z, y)
        return amplx*amply, phasex+phasey


class HermiteGaussBeam(NormalizedHermiteGaussBeam):
    name = 'HermiteGaussBeam'

    # 振幅, 波长, 束腰位置, x方向束腰半径, y方向束腰半径, x方向模式数, y方向模式数
    modifiable_properties = ('A0', 'wavelength', 'p0',
                             'omega0x', 'omega0y', 'mx', 'my')

    def __init__(self, name='HermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required('A0')
        self.property_set['A0'] = kwargs.get('A0', None)

    @property
    def A0(self):
        """振幅"""
        return self.get_property('A0')

    def A_f(self, z):
        """振幅函数"""
        A0 = self.A0
        A = super().A_f(z)
        return A0*A


class NormalizedGaussBeam(NormalizedHermiteGaussBeam):
    name = 'NormalizedGaussBeam'

    modifiable_properties = ('wavelength', 'p0', 'omega0x', 'omega0y')

    def __init__(self, name='NormalizedGaussBeam', **kwargs):
        kwargs.update(mx=0, my=0)

        super().__init__(**kwargs)
        self.name = name


class GaussBeam(HermiteGaussBeam):
    name = 'HermiteGaussBeam'

    modifiable_properties = ('A0', 'wavelength', 'p0', 'omega0x', 'omega0y')

    def __init__(self, name='HermiteGaussBeam', **kwargs):
        kwargs.update(mx=0, my=0)

        super().__init__(**kwargs)
        self.name = name


class NormalizedAxisymmetricHermiteGaussBeam(NormalizedHermiteGaussBeam1D):
    name = 'NormalizedAxisymmetricHermiteGaussBeam'

    # 波长, 束腰半径, 束腰位置, 模式数
    modifiable_properties = ('wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='NormalizedAxisymmetricHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(
            NormalizedAxisymmetricHermiteGaussBeam.modifiable_properties)

        for prop in NormalizedAxisymmetricHermiteGaussBeam.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def c(self):
        """总归一化因子"""
        return self.get_property('c', lambda: (super(NormalizedAxisymmetricHermiteGaussBeam, self).c)**2)

    def A_f(self, z):
        """振幅函数"""
        return (super().A_f(z))**2

    def u_f(self, z, x, y):
        """强度函数"""
        c = self.c
        A = self.A_f(z)
        psi = self.psi_f(z, x)*self.psi_f(z, y)
        phi = self.phi_f(z)
        k = self.k
        R = self.R_f(z)
        m = self.m

        ampl = c*A*psi
        phase = -k/(2*R)*(x**2+y**2)+(2*m+1/2)*phi

        return ampl, phase


class AxisymmetricHermiteGaussBeam(NormalizedAxisymmetricHermiteGaussBeam):
    name = 'AxisymmetricHermiteGaussBeam'

    modifiable_properties = ('A0', 'p0', 'wavelength', 'omega0', 'm')

    def __init__(self, name='AxisymmetricHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required('A0')
        self.property_set['A0'] = kwargs.get('A0', None)

    @property
    def A0(self):
        """振幅"""
        return self.get_property('A0')

    def A_f(self, z):
        """振幅函数"""
        A0 = self.A0
        A = super().A_f(z)
        return A0*A


class NormalizedAxisymmetricGaussBeam(NormalizedAxisymmetricHermiteGaussBeam):
    name = 'NormalizedAxisymmetricGaussBeam'

    modifiable_properties = ('wavelength', 'p0', 'omega0')

    def __init__(self, name='NormalizedAxisymmetricGaussBeam', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


class AxisymmetricGaussBeam(AxisymmetricHermiteGaussBeam):
    name = 'AxisymmetricGaussBeam'

    modifiable_properties = ('A0', 'wavelength', 'p0', 'omega0')

    def __init__(self, name='AxisymmetricGaussBeam', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


def local2remote(wavelength, omega0, z):
    """
    已知波长和基模束腰半径，计算一定位置处的基模模场半径。
    默认束腰在原点，且坐标轴正方向的曲率半径为正。此函数可以直接用于高阶模式。
    :param wavelength: 波长
    :param omega0: 基模束腰半径
    :param z: 距离
    :return: (omega, R)基模模场半径和曲率半径
    """
    zr = constants.pi * omega0 ** 2 / wavelength
    omega = omega0 * np.sqrt(1 + (z / zr) ** 2)
    R = z * (1 + (zr / z) ** 2)
    return omega, R


def remote2local(wavelength, omega, R):
    """
    已知波长、基模模场半径和曲率半径，计算基模束腰半径和位置。
    默认束腰在原点，且坐标轴正方向的曲率半径为正。此函数可以直接用于高阶模式。
    此函数可以直接用于高阶模式。
    :param wavelength: 波长
    :param omega: 基模模场半径
    :param R: 曲率半径
    :return: (omega0, z)基模束腰半径和位置
    """
    zrp = constants.pi * omega ** 2 / wavelength
    omega0 = omega / np.sqrt(1 + (zrp / R) ** 2)
    z = R / (1 + (R / zrp) ** 2)
    return omega0, z


def convert_through_mirror(wavelength, omega0, s, roc):
    """
    计算通过镜面反射后的Hermite-Gaussian光，且默认此镜面是轴对称的
    :param wavelength: 波长
    :param omega0: 基模束腰半径
    :param s: 束腰相对于镜面的位置，且认为镜面在原点处，通常束腰在镜面左边为负。
    :param roc: 镜面的曲率半径
    :return: (omega0p, sp)反射后的束腰半径和位置
    """
    omega0p, spm = convert_through_lens(wavelength, omega0, s, roc/2)
    sp = -spm
    return omega0p, sp

def convert_through_lens(wavelength, omega0, s, f):
    """
    计算通过透镜后的Hermite-Gaussian光，且默认此透镜是轴对称的
    :param wavelength: 波长
    :param omega0: 基模束腰半径
    :param s: 束腰相对于镜面的位置，且认为透镜在原点处，通常束腰在镜面左边为负。
    :param f: 透镜的焦距
    :return: (omega0p, sp)透射后的束腰半径和位置
    """
    omegap, R = local2remote(wavelength, omega0, s)
    Rp = 1 / (1 / R + 1 / f)
    omega0p, sp = remote2local(wavelength, omegap, Rp)
    return omega0p, sp

