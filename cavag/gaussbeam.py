import scipy as sp
from scipy import constants
from scipy import special
from ._utils import PrintableObject, PropertySet

__all__ = [
    'GaussBeam',
    'convert_through_mirror',
    'local2remote',
    'remote2local',
    'get_spot_info_after_deviation'
]


class NormalizedHermiteGaussBeam1D(PrintableObject):
    name = 'HermiteGaussBeam1D'

    def __init__(self, wavelength, omega0, p0, m, name='NormalizedHermiteGaussBeam1D', **kwargs):
        self.name = name

        # 波长, 束腰半径, 束腰位置, 模式数
        self.property_set = PropertySet(('wavelength', 'omega0', 'p0', 'm'))
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0'] = omega0
        self.property_set['p0'] = p0
        self.property_set['m'] = m
        self.property_set.update(kwargs)

    @property
    def c(self):
        """归一化因子"""
        if 'c' not in self.property_set:
            self.property_set['c'] = (2/constants.pi)**(1/4)/sp.sqrt(omega0*(2**m)*special.factorial(m))
        return self.property_set['c']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set['wavelength']
    
    @property
    def k(self):
        """波矢"""
        if 'k' not in self.property_set:
            self.property_set['k'] = 2*constants.pi/self.wavelength
        return self.property_set['k']

    @property
    def omega0(self):
        """束腰半径"""
        return self.property_set['omega0']
    
    @property
    def p0(self):
        """束腰位置"""
        return self.property_set['p0']
    
    @property
    def m(self) -> int:
        """Hermite-Gaussian光的模式"""
        return self.property_set['m']

    @property
    def z0(self):
        """瑞利长度"""
        if 'z0' not in self.property_set:
            self.property_set['z0'] = constants.pi * (self.omega0) ** 2 / self.wavelength
        return self.property_set['z0']
    
    @property
    def h_f(self):
        """Hermite多项式"""
        if 'h_f' not in self.property_set:
            self.property_set['h_f'] = special.hermite(self.m)
        return self.property_set['h_f']
    
    def A_f(self, z):
        z0, p0 = self.z0, self.p0
        return 1/(1+((z-p0)/z0)**2)**(1/4)

    def omega_f(self, z):
        omega0, z0, p0 = self.omega0, self.z0, self.p0
        return omega0*sp.sqrt(1 + ((z-p0)/z0)**2)
    
    def R_f(self, z):
        z0, p0 = self.z0, self.p0
        return (z-p0)*(1+(z0/(z-p0))**2)
    
    def phi_f(self, z):
        z0, p0 = self.z0, self.p0
        return sp.arctan((z-p0)/z0)
    
    def psi_f(self, x, z):
        h_f = self.h_f
        omega = self.omega_f(z)
        xi = sp.sqrt(2)*x/omega

        return h_f(xi)*sp.exp(-xi**2/2)
    
    def u_f(self, x, z):
        c = self.c
        A = self.A_f(z)
        psi = self.psi_f(x, z)
        phi = self.phi_f(z)
        k = self.k
        R = self.R_f(z)
        m = self.m

        ampl = c*A*psi
        phase = -k/(2*R)*x**2+(m+1/2)*phi

        return ampl, phase

class NormalizedHermiteGaussBeam(PrintableObject):
    name = 'HermiteGaussBeam'

    def __init__(self, A0, wavelength, omega0x, omega0y, cx, cy, name='HermiteGaussBeam1D', **kwargs):
        self.name = name

        # 振幅, 波长, x方向束腰半径, y方向束腰半径
        self.property_set = PropertySet(('A0', 'wavelength', 'omega0x', 'omega0y', 'cx', 'cy'))
        self.property_set['A0'] = A0
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0x'] = omega0x
        self.property_set['omega0y'] = omega0y
        self.property_set['cx'] = cx
        self.property_set['cy'] = cy
        self.property_set.update(kwargs)

    @property
    def A0(self):
        """振幅"""
        return self.property_set['A0']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set['wavelength']

    @property
    def omega0x(self):
        """x方向束腰半径"""
        return self.property_set['omega0x']
    
    @property
    def omega0y(self):
        """y方向束腰半径"""
        return self.property_set['omega0y']
    
    @property
    def cx(self):
        """x方向束腰位置"""
        return self.property_set['cx']
    
    @property
    def cy(self):
        """y方向束腰位置"""
        return self.property_set['cy']

    @property
    def z0x(self):
        """x方向瑞利长度"""
        return sp.pi * (self.omega0x) ** 2 / self.wavelength
    
    @property
    def z0y(self):
        """y方向瑞利长度"""
        return sp.pi * (self.omega0y) ** 2 / self.wavelength


class HermiteGaussBeam(PrintableObject):
    name = 'HermiteGaussBeam'

    def __init__(self, A0, wavelength, omega0x, omega0y, cx, cy, name='HermiteGaussBeam', **kwargs):
        self.name = name

        # 振幅, 波长, x方向束腰半径, y方向束腰半径
        self.property_set = PropertySet(('A0', 'wavelength', 'omega0x', 'omega0y', 'cx', 'cy'))
        self.property_set['A0'] = A0
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0x'] = omega0x
        self.property_set['omega0y'] = omega0y
        self.property_set['cx'] = cx
        self.property_set['cy'] = cy
        self.property_set.update(kwargs)

    @property
    def A0(self):
        """振幅"""
        return self.property_set['A0']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set['wavelength']

    @property
    def omega0x(self):
        """x方向束腰半径"""
        return self.property_set['omega0x']
    
    @property
    def omega0y(self):
        """y方向束腰半径"""
        return self.property_set['omega0y']
    
    @property
    def cx(self):
        """x方向束腰位置"""
        return self.property_set['cx']
    
    @property
    def cy(self):
        """y方向束腰位置"""
        return self.property_set['cy']

    @property
    def z0x(self):
        """x方向瑞利长度"""
        return sp.pi * (self.omega0x) ** 2 / self.wavelength
    
    @property
    def z0y(self):
        """y方向瑞利长度"""
        return sp.pi * (self.omega0y) ** 2 / self.wavelength



class HermiteGaussBeam2D(Position):
    name = 'GaussBeam1D'

    def __init__(self, A0, wavelength, omega0, position, name='HermiteGaussBeam1D', **kwargs):
        super(Position, self).__init__(position=position)
        self.name = name

        # 振幅, 波长, 束腰半径
        self.property_set.add_required(('A0', 'wavelength', 'omega0'))
        self.property_set['A0'] = A0
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0'] = omega0
        self.property_set['position'] = position
        self.property_set.update(kwargs)

    @property
    def position(self):
        """束腰位置"""
        return self.property_set['position']

    @property
    def z0(self):
        """瑞利长度"""
        return sp.pi * (self.omega0) ** 2 / self.wavelength

    @property
    def A0(self):
        """振幅"""
        return self.property_set['A0']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set['wavelength']

    @property
    def omega0(self):
        """束腰半径"""
        return self.property_set['omega0']


class SymmetricHermiteGaussBeam2D(Position):
    name = 'GaussBeam1D'

    def __init__(self, A0, wavelength, omega0, position, name='HermiteGaussBeam1D', **kwargs):
        super(Position, self).__init__(position=position)
        self.name = name

        # 振幅, 波长, 束腰半径
        self.property_set.add_required(('A0', 'wavelength', 'omega0'))
        self.property_set['A0'] = A0
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0'] = omega0
        self.property_set['position'] = position
        self.property_set.update(kwargs)

    @property
    def position(self):
        """束腰位置"""
        return self.property_set['position']

    @property
    def z0(self):
        """瑞利长度"""
        return sp.pi * (self.omega0) ** 2 / self.wavelength

    @property
    def A0(self):
        """振幅"""
        return self.property_set['A0']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set['wavelength']

    @property
    def omega0(self):
        """束腰半径"""
        return self.property_set['omega0']


class GaussBeam1D(Position):
    name = 'GaussBeam1D'

    def __init__(self, A0, wavelength, omega0, position, name='GaussBeam1D', **kwargs):
        super(Position, self).__init__(position=position)
        self.name = name

        # 振幅, 波长, 束腰半径
        self.property_set.add_required(('A0', 'wavelength', 'omega0'))
        self.property_set['A0'] = A0
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0'] = omega0
        self.property_set['position'] = position
        self.property_set.update(kwargs)

    @property
    def position(self):
        """束腰位置"""
        return self.property_set['position']

    @property
    def z0(self):
        """瑞利长度"""
        return sp.pi * (self.omega0) ** 2 / self.wavelength

    @property
    def A0(self):
        """振幅"""
        return self.property_set['A0']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set['wavelength']

    @property
    def omega0(self):
        """束腰半径"""
        return self.property_set['omega0']

class GaussBeam2D(Position):
    name = 'GaussBeam'

    def __init__(self, A0, wavelength, omega0, position, name='GaussBeam', **kwargs):
        super(Position, self).__init__(position=position)
        self.name = name

        # 振幅, 波长, 束腰半径
        self.property_set.add_required(('A0', 'wavelength', 'omega0'))
        self.property_set['A0'] = A0
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0'] = omega0
        self.property_set['position'] = position
        self.property_set.update(kwargs)

    @property
    def position(self):
        """束腰位置"""
        return self.property_set['position']

    @property
    def z0(self):
        """瑞利长度"""
        return sp.pi * (self.omega0) ** 2 / self.wavelength

    @property
    def A0(self):
        """振幅"""
        return self.property_set['A0']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set['wavelength']

    @property
    def omega0(self):
        """束腰半径"""
        return self.property_set['omega0']


def convert_through_mirror(beam, mirror):
    """记发散为负，会聚为正"""
    fp = mirror.f
    wavelength = beam.wavelength
    s = beam.position - mirror.position
    omegap, R = local2remote(beam.omega0, s, wavelength)
    Rp = 1 / (1 / R + 1 / fp)
    omega0p, spc = remote2local(omegap, Rp, wavelength)
    return GaussBeam(spc + mirror.position, omega0p, beam.A0 * beam.omega0 / omega0p, wavelength)


def local2remote(omega0, s, wavelength):
    zr = constants.pi * omega0 ** 2 / wavelength
    omega = omega0 * sp.sqrt(1 + (s / zr) ** 2)
    R = s * (1 + (zr / s) ** 2)
    return omega, R


def remote2local(omega, R, wavelength):
    zrp = constants.pi * omega ** 2 / wavelength
    omega0 = omega / sp.sqrt(1 + (zrp / R) ** 2)
    s = R / (1 + (R / zrp) ** 2)
    return omega0, s


def get_spot_info_after_deviation(beam, z):
    zr = constants.pi * beam.omega0 ** 2 / beam.wavelength
    R = z * (1 + (zr / z) ** 2)
    omega = beam.omega0 * sp.sqrt(1 + (z / zr) ** 2)
    A = beam.A0 * beam.omega0 / omega
    return omega, R, A

