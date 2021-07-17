from math import sqrt
import numpy as np
from scipy import constants
from scipy import special
from .misc import Wavelength

__all__ = [
    'NormalizedHermiteGaussBeam1D', 'HermiteGaussBeam1D',
    'NormalizedGaussBeam1D', 'GaussBeam1D',
    'NormalizedHermiteGaussBeam', 'HermiteGaussBeam',
    'NormalizedGaussBeam', 'GaussBeam',
    'NormalizedEqualHermiteGaussBeam', 'EqualHermiteGaussBeam',
    'NormalizedEqualSymmetricHermiteGaussBeam', 'EqualSymmetricHermiteGaussBeam',
    'NormalizedEqualGaussBeam', 'EqualGaussBeam',
    'local2remote', 'remote2local', 'convert_through_lens', 'convert_through_mirror'
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
    def cm(self):
        """归一化因子[1]"""
        def v_f():
            omega0 = self.omega0
            m = self.m
            return (2/constants.pi)**(1/4)/np.sqrt(omega0*(2**m)*special.factorial(m))
        return self.get_property('cm', v_f)

    @property
    def p0(self):
        """束腰位置[L]"""
        return self.get_property('p0')

    @property
    def omega0(self):
        """等价基模束腰半径[L]"""
        return self.get_property('omega0')

    @property
    def omega0m(self):
        """束腰半径[L]"""
        return self.get_property('omega0m', lambda: np.sqrt(2*self.m+1)*self.omega0)

    @property
    def m(self) -> int:
        """光的模式数[1]"""
        return self.get_property('m')

    @property
    def z0(self):
        """瑞利长度[L]"""
        return self.get_property('z0', lambda:  constants.pi * (self.omega0) ** 2 / self.wavelength)

    @property
    def thetam(self):
        """半发散角[1]"""
        return self.get_property('thetam', lambda: np.sqrt(2*self.m+1)*np.arctan(self.wavelength/(constants.pi*self.omega0)))

    @property
    def hm(self):
        """Hermite多项式"""
        return self.get_property('hm', lambda:  special.hermite(self.m))

    def a_f(self, z):
        """振幅函数"""
        z0, p0 = self.z0, self.p0
        return 1/(1+((z-p0)/z0)**2)**(1/4)

    def omega_f(self, z):
        """等价基模半径函数"""
        omega0, z0, p0 = self.omega0, self.z0, self.p0
        return omega0*np.sqrt(1 + ((z-p0)/z0)**2)

    def omegam_f(self, z):
        """模场半径函数"""
        omega = self.omega_f(z)
        return np.sqrt(2*self.m+1)*omega

    def r_f(self, z):
        """波前曲率半径函数"""
        z0, p0 = self.z0, self.p0
        return (z-p0)*(1+(z0/(z-p0))**2)

    def phi_f(self, z):
        """phi相位函数"""
        z0, p0 = self.z0, self.p0
        return np.arctan((z-p0)/z0)

    def psim_f(self, z, x):
        """HG函数"""
        hm = self.hm
        omega = self.omega_f(z)
        xi = np.sqrt(2)*x/omega

        return hm(xi)*np.exp(-xi**2/2)

    def u_f(self, z, x):
        """强度函数"""
        cm = self.cm
        a = self.a_f(z)
        psi = self.psim_f(z, x)
        phi = self.phi_f(z)
        k = self.k
        r = self.r_f(z)
        m = self.m

        ampl = cm*a*psi
        phase = -k/(2*r)*x**2+(m+1/2)*phi

        return ampl, phase


class HermiteGaussBeam1D(NormalizedHermiteGaussBeam1D):
    name = 'HermiteGaussBeam1D'

    # 振幅, 波长, 束腰位置, 等价基模束腰半径, 模式数
    modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='HermiteGaussBeam1D', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required('a0')
        self.property_set['a0'] = kwargs.get('a0', None)

    @property
    def a0(self):
        """振幅"""
        return self.get_property('a0')

    def a_f(self, z):
        """振幅函数"""
        a0 = self.a0
        a = super().a_f(z)
        return a0*a


class NormalizedGaussBeam1D(NormalizedHermiteGaussBeam1D):
    name = 'NormalizedGaussBeam1D'

    modifiable_properties = ('wavelength', 'omega0', 'p0')

    def __init__(self, name='NormalizedGaussBeam1D', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


class GaussBeam1D(HermiteGaussBeam1D):
    name = 'GaussBeam1D'

    modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0')

    def __init__(self, name='GaussBeam1D', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


class NormalizedHermiteGaussBeam(Wavelength):
    name = 'NormalizedHermiteGaussBeam'

    # 波长, 束腰位置, x方向等价基模束腰半径, y方向等价基模束腰半径, x方向模式数, y方向模式数
    modifiable_properties = (
        'wavelength', 'p0', 'omega0x', 'omega0y', 'mx', 'my')

    def __init__(self, name='NormalizedHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(
            NormalizedHermiteGaussBeam.modifiable_properties)

        for prop in NormalizedHermiteGaussBeam.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

        # beam cache
        self.__beams = {'x': None, 'y': None}

    def change_params(self, *args, **kwargs):
        self.__beams['x'] = None
        self.__beams['y'] = None
        super().change_params(*args, **kwargs)

    def __get_beam(self, d):
        if self.__beams[d]:
            beam = self.__beams[d]
        else:
            beam = NormalizedHermiteGaussBeam1D(
                wavelength=self.wavelength, p0=self.p0,
                omega0=getattr(self, 'omega0'+d), m=getattr(self, 'm'+d)
            )
            self.__beams[d] = beam
        return beam

    @property
    def cmx(self):
        """x方向归一化因子"""
        return self.get_property('cmx', lambda: self.__get_beam('x').cm)

    @property
    def cmy(self):
        """y方向归一化因子"""
        return self.get_property('cmy', lambda: self.__get_beam('y').cm)

    @property
    def cm(self):
        """总归一化因子"""
        return self.get_property('cm', lambda: self.cmx*self.cmy)

    @property
    def p0(self):
        """束腰位置[L]"""
        return self.get_property('p0')

    @property
    def omega0x(self):
        """x方向等价基模束腰半径[L]"""
        return self.get_property('omega0x')

    @property
    def omega0y(self):
        """y方向等价基模束腰半径[L]"""
        return self.get_property('omega0y')

    @property
    def omega0mx(self):
        """x方向模场束腰半径[L]"""
        return self.get_property('omega0mx', lambda: self.__get_beam('x').omega0m)

    @property
    def omega0my(self):
        """y方向模场束腰半径[L]"""
        return self.get_property('omega0my', lambda: self.__get_beam('y').omega0m)

    @property
    def thetamx(self):
        """x方向半发散角[1]"""
        return self.get_property('thetamx', lambda: self.__get_beam('x').thetam)

    @property
    def thetamy(self):
        """y方向半发散角[1]"""
        return self.get_property('thetamy', lambda: self.__get_beam('y').thetam)

    @property
    def mx(self) -> int:
        """x方向光的模式数[1]"""
        return self.get_property('mx')

    @property
    def my(self) -> int:
        """y方向光的模式数[1]"""
        return self.get_property('my')

    @property
    def z0x(self):
        """x方向瑞利长度[L]"""
        return self.get_property('z0x', lambda: self.__get_beam('x').z0)

    @property
    def z0y(self):
        """y方向瑞利长度[L]"""
        return self.get_property('z0y', lambda: self.__get_beam('y').z0)

    @property
    def hmx(self):
        """x方向Hermite多项式"""
        return self.get_property('hmx', lambda: self.__get_beam('x').hm)

    @property
    def hmy(self):
        """y方向Hermite多项式"""
        return self.get_property('hmy', lambda: self.__get_beam('y').hm)

    def a_f(self, z):
        """振幅函数"""
        return (self.__get_beam('x').a_f(z))*(self.__get_beam('y').a_f(z))

    def omegax_f(self, z):
        """x方向等价基模半径函数"""
        return self.__get_beam('x').omega_f(z)

    def omegay_f(self, z):
        """y方向等价基模半径函数"""
        return self.__get_beam('y').omega_f(z)

    def omegamx_f(self, z):
        """x方向模场半径函数"""
        return self.__get_beam('x').omegam_f(z)

    def omegamy_f(self, z):
        """y方向模场半径函数"""
        return self.__get_beam('y').omegam_f(z)

    def rx_f(self, z):
        """x方向波前曲率半径函数"""
        return self.__get_beam('x').r_f(z)

    def ry_f(self, z):
        """y方向波前曲率半径函数"""
        return self.__get_beam('y').r_f(z)

    def phix_f(self, z):
        """x方向phi相位函数"""
        return self.__get_beam('x').phi_f(z)

    def phiy_f(self, z):
        """y方向phi相位函数"""
        return self.__get_beam('y').phi_f(z)

    def psimx_f(self, z, x):
        """x方向HG函数"""
        return self.__get_beam('x').psim_f(z, x)

    def psimy_f(self, z, y):
        """y方向HG函数"""
        return self.__get_beam('y').psim_f(z, y)

    def u_f(self, z, x, y):
        """强度函数"""
        amplx, phasex = self.__get_beam('x').u_f(z, x)
        amply, phasey = self.__get_beam('y').u_f(z, y)
        return amplx*amply, phasex+phasey


class HermiteGaussBeam(NormalizedHermiteGaussBeam):
    name = 'HermiteGaussBeam'

    # 振幅, 波长, 束腰位置, x方向等价基模束腰半径, y方向等价基模束腰半径, x方向模式数, y方向模式数
    modifiable_properties = ('a0', 'wavelength', 'p0',
                             'omega0x', 'omega0y', 'mx', 'my')

    def __init__(self, name='HermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required('a0')
        self.property_set['a0'] = kwargs.get('a0', None)

    @property
    def a0(self):
        """振幅"""
        return self.get_property('a0')

    def a_f(self, z):
        """振幅函数"""
        a0 = self.a0
        a = super().a_f(z)
        return a0*a


class NormalizedGaussBeam(NormalizedHermiteGaussBeam):
    name = 'NormalizedGaussBeam'

    modifiable_properties = ('wavelength', 'p0', 'omega0x', 'omega0y')

    def __init__(self, name='NormalizedGaussBeam', **kwargs):
        kwargs.update(mx=0, my=0)

        super().__init__(**kwargs)
        self.name = name


class GaussBeam(HermiteGaussBeam):
    name = 'HermiteGaussBeam'

    modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0x', 'omega0y')

    def __init__(self, name='HermiteGaussBeam', **kwargs):
        kwargs.update(mx=0, my=0)

        super().__init__(**kwargs)
        self.name = name


class NormalizedEqualHermiteGaussBeam(NormalizedHermiteGaussBeam):
    name = 'NormalizedEqualHermiteGaussBeam'

    # 波长, 束腰位置, 等价基模束腰半径, x方向模式数, y方向模式数
    modifiable_properties = ('wavelength', 'p0', 'omega0', 'mx', 'my')

    def __init__(self, name="NormalizedEqualHermiteGaussBeam", **kwargs):
        omega0 = kwargs.get('omega0', None)
        kwargs['omega0x'] = kwargs['omega0y'] = omega0
        super().__init__(**kwargs)

        self.name = name

        self.property_set.add_required('omega0')
        self.property_set['omega0'] = kwargs.get('omega0', None)

    @property
    def omega0(self):
        """等价基模束腰半径"""
        return self.get_property('omega0')

    @property
    def z0(self):
        """瑞利长度[L]"""
        return self.get_property('z0', lambda: self.z0x)

    def omega_f(self, z):
        """等价基模半径函数"""
        return self.omegax_f(z)

    def r_f(self, z):
        """波前曲率半径函数"""
        return self.rx_f(z)

    def phi_f(self, z):
        """phi相位函数"""
        return self.phix_f(z)

    def preprocess_properties(self, **propdict):
        if 'omega0' in propdict:
            propdict['omega0x'] = propdict['omega0y'] = propdict['omega0']

        propdict = super().preprocess_properties(**propdict)

        return propdict


class EqualHermiteGaussBeam(NormalizedEqualHermiteGaussBeam):
    name = 'EqualHermiteGaussBeam'

    # 振幅, 波长, 束腰位置, 等价基模束腰半径, x方向模式数, y方向模式数
    modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0', 'mx', 'my')

    def __init__(self, name='EqualHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required('a0')
        self.property_set['a0'] = kwargs.get('a0', None)

    @property
    def a0(self):
        """振幅"""
        return self.get_property('a0')

    def a_f(self, z):
        """振幅函数"""
        a0 = self.a0
        a = super().a_f(z)
        return a0*a


class NormalizedEqualSymmetricHermiteGaussBeam(NormalizedHermiteGaussBeam1D):
    name = 'NormalizedEqualSymmetricHermiteGaussBeam'

    # 波长, 束腰位置, 等价基模束腰半径, 模式数
    modifiable_properties = ('wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='NormalizedEqualSymmetricHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(
            NormalizedEqualSymmetricHermiteGaussBeam.modifiable_properties)

        for prop in NormalizedEqualSymmetricHermiteGaussBeam.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

    @property
    def cm(self):
        """总归一化因子"""
        return self.get_property('cm', lambda: (super(NormalizedEqualSymmetricHermiteGaussBeam, self).cm)**2)

    def a_f(self, z):
        """振幅函数"""
        return (super().a_f(z))**2

    def u_f(self, z, x, y):
        """强度函数"""
        cm = self.cm
        a = self.a_f(z)
        psi = self.psim_f(z, x)*self.psim_f(z, y)
        phi = self.phi_f(z)
        k = self.k
        r = self.r_f(z)
        m = self.m

        ampl = cm*a*psi
        phase = -k/(2*r)*(x**2+y**2)+(2*m+1/2)*phi

        return ampl, phase


class EqualSymmetricHermiteGaussBeam(NormalizedEqualSymmetricHermiteGaussBeam):
    name = 'EqualSymmetricHermiteGaussBeam'

    modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='EqualSymmetricHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required('a0')
        self.property_set['a0'] = kwargs.get('a0', None)

    @property
    def a0(self):
        """振幅"""
        return self.get_property('a0')

    def a_f(self, z):
        """振幅函数"""
        a0 = self.a0
        a = super().a_f(z)
        return a0*a


class NormalizedEqualGaussBeam(NormalizedEqualSymmetricHermiteGaussBeam):
    name = 'NormalizedEqualGaussBeam'

    modifiable_properties = ('wavelength', 'p0', 'omega0')

    def __init__(self, name='NormalizedEqualGaussBeam', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


class EqualGaussBeam(EqualSymmetricHermiteGaussBeam):
    name = 'EqualGaussBeam'

    modifiable_properties = ('a0', 'wavelength', 'p0', 'omega0')

    def __init__(self, name='EqualGaussBeam', **kwargs):
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
    :return: (omega, r)基模模场半径和曲率半径
    """
    zr = constants.pi * omega0 ** 2 / wavelength
    omega = omega0 * np.sqrt(1 + (z / zr) ** 2)
    r = z * (1 + (zr / z) ** 2)
    return omega, r


def remote2local(wavelength, omega, r):
    """
    已知波长、基模模场半径和曲率半径，计算基模束腰半径和位置。
    默认束腰在原点，且坐标轴正方向的曲率半径为正。此函数可以直接用于高阶模式。
    :param wavelength: 波长
    :param omega: 基模模场半径
    :param r: 曲率半径
    :return: (omega0, z)基模束腰半径和位置
    """
    zrp = constants.pi * omega ** 2 / wavelength
    omega0 = omega / np.sqrt(1 + (zrp / r) ** 2)
    z = r / (1 + (r / zrp) ** 2)
    return omega0, z


def convert_through_lens(wavelength, omega0, s, f):
    """
    计算通过透镜后的Hermite-Gaussian光，且默认此透镜是轴对称的
    :param wavelength: 波长
    :param omega0: 基模束腰半径
    :param s: 束腰相对于镜面的位置，且认为透镜在原点处，通常束腰在镜面左边为负。
    :param f: 透镜的焦距
    :return: (omega0p, sp)透射后的束腰半径和位置
    """
    omegap, r = local2remote(wavelength, omega0, s)
    rp = 1 / (1 / r + 1 / f)
    omega0p, sp = remote2local(wavelength, omegap, rp)
    return omega0p, sp


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
