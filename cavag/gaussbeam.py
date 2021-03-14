import scipy as sp
from scipy import constants
from scipy import special
from ._utils import PrintableObject, PropertySet

__all__ = [
    'NormalizedHermiteGaussBeam1D', 'HermiteGaussBeam1D',
    'NormalizedGaussBeam1D', 'GaussBeam1D',
    'NormalizedHermiteGaussBeam2D', 'HermiteGaussBeam2D',
    'NormalizedGaussBeam2D', 'GaussBeam2D',
    'NormalizedSymmetricHermiteGaussBeam', 'SymmetricHermiteGaussBeam',
    'NormalizedSymmetricGaussBeam', 'SymmetricGaussBeam'
]


class NormalizedHermiteGaussBeam1D(PrintableObject):
    name = 'NormalizedHermiteGaussBeam1D'

    # 波长, 束腰半径, 束腰位置, 模式数
    modifiable_properties = ('wavelength', 'omega0', 'p0', 'm')

    def __init__(self, wavelength, omega0, p0, m, name='NormalizedHermiteGaussBeam1D'):
        self.name = name

        self.property_set = PropertySet(NormalizedHermiteGaussBeam1D.modifiable_properties)
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0'] = omega0
        self.property_set['p0'] = p0
        self.property_set['m'] = m

    @property
    def c(self):
        """归一化因子"""
        if 'c' not in self.property_set:
            self.property_set['c'] = (2/constants.pi)**(1/4)/sp.sqrt(omega0*(2**m)*special.factorial(m))
        return self.property_set['c']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set.get_strictly('wavelength')
    
    @property
    def k(self):
        """波矢"""
        if 'k' not in self.property_set:
            self.property_set['k'] = 2*constants.pi/self.wavelength
        return self.property_set['k']

    @property
    def omega0(self):
        """束腰半径"""
        return self.property_set.get_strictly('omega0')
    
    @property
    def p0(self):
        """束腰位置"""
        return self.property_set.get_strictly('p0')
    
    @property
    def m(self) -> int:
        """Hermite-Gaussian光的模式"""
        return self.property_set.get_strictly('m')

    @property
    def z0(self):
        """瑞利长度"""
        if 'z0' not in self.property_set:
            self.property_set['z0'] = constants.pi * (self.omega0) ** 2 / self.wavelength
        return self.property_set['z0']
    
    @property
    def hm(self):
        """Hermite多项式"""
        if 'hm' not in self.property_set:
            self.property_set['hm'] = special.hermite(self.m)
        return self.property_set['hm']
    
    def A_f(self, z):
        """振幅函数"""
        z0, p0 = self.z0, self.p0
        return 1/(1+((z-p0)/z0)**2)**(1/4)

    def omega_f(self, z):
        """模场半径函数"""
        omega0, z0, p0 = self.omega0, self.z0, self.p0
        return omega0*sp.sqrt(1 + ((z-p0)/z0)**2)
    
    def R_f(self, z):
        """波前曲率半径函数"""
        z0, p0 = self.z0, self.p0
        return (z-p0)*(1+(z0/(z-p0))**2)
    
    def phi_f(self, z):
        """相位函数"""
        z0, p0 = self.z0, self.p0
        return sp.arctan((z-p0)/z0)
    
    def psi_f(self, z, x):
        """Hermite-Gaussian模式"""
        hm = self.hm
        omega = self.omega_f(z)
        xi = sp.sqrt(2)*x/omega

        return hm(xi)*sp.exp(-xi**2/2)
    
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

    # 振幅, 波长, 束腰半径, 束腰位置, 模式数
    modifiable_properties = ('A0', 'wavelength', 'omega0', 'p0', 'm')

    def __init__(self, A0, wavelength, omega0, p0, m, name='HermiteGaussBeam1D'):
        super().__init__(wavelength, omega0, p0, m)
        self.name = name
        
        self.property_set.add_required('A0')
        self.property_set['A0'] = A0

    @property
    def A0(self):
        """振幅"""
        return self.property_set.get_strictly('A0')

    def A_f(self, z):
        """振幅函数"""
        A0 = self.A0
        A = super().A_f(z)
        return A0*A


class NormalizedGaussBeam1D(NormalizedHermiteGaussBeam1D):
    name = 'NormalizedGaussBeam1D'

    # 波长, 束腰半径, 束腰位置
    modifiable_properties = ('wavelength', 'omega0', 'p0')

    def __init__(self, wavelength, omega0, p0, name='NormalizedGaussBeam1D'):
        super().__init__(wavelength, omega0, p0, m=0)
        self.name = name


class GaussBeam1D(HermiteGaussBeam1D):
    name = 'GaussBeam1D'

    # 振幅, 波长, 束腰半径, 束腰位置
    modifiable_properties = ('A0', 'wavelength', 'omega0', 'p0')

    def __init__(self, A0, wavelength, omega0, p0, name='GaussBeam1D'):
        super().__init__(A0, wavelength, omega0, p0, m=0)
        self.name = name


class NormalizedHermiteGaussBeam2D(PrintableObject):
    name = 'NormalizedHermiteGaussBeam2D'

    # 波长, x方向束腰半径, y方向束腰半径, x方向束腰位置, y方向束腰位置, x方向模式数, y方向模式数
    modifiable_properties = ('wavelength', 'omega0x', 'omega0y', 'p0x', 'p0y', 'mx', 'my')

    def __init__(self, wavelength, omega0x, omega0y, p0x, p0y, mx, my, name='NormalizedHermiteGaussBeam2D'):
        self.name = name

        self.property_set = PropertySet(NormalizedHermiteGaussBeam2D.modifiable_properties)
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0x'] = omega0x
        self.property_set['omega0y'] = omega0y
        self.property_set['p0x'] = p0x
        self.property_set['p0y'] = p0y
        self.property_set['mx'] = mx
        self.property_set['my'] = my

        self.__beams = (
            NormalizedHermiteGaussBeam1D(wavelength, omega0x, p0x, mx, 'x-direction'),
            NormalizedHermiteGaussBeam1D(wavelength, omega0y, p0y, my, 'y-direction'),
        )
    
    def change_params(self, _filter=True, **kwargs):
        if _filter:
            kwargs = self.filter_properties(kwargs)

        self.property_set.change_params(**kwargs)
        xkw, ykw = {}, {}
        for k, v in kwargs:
            if k.endswith('x')
                xkw[k[:-1]] = v
            elif k.endswith('y'):
                ykw[k[:-1]] = v
            else:
                xkw[k] = v
                ykw[k] = v
            
        if xkw:
            self.__beams[0].change_params(**xkw)
        if ykw:
            self.__beams[1].change_params(**xkw)

    @property
    def cx(self):
        """x方向归一化因子"""
        if 'cx' not in self.property_set:
            self.property_set['cx'] = self.__beams[0].c
        return self.property_set['cx']
    
    @property
    def cy(self):
        """y方向归一化因子"""
        if 'cy' not in self.property_set:
            self.property_set['cy'] = self.__beams[1].c
        return self.property_set['cy']
    
    @property
    def c(self):
        """归一化因子"""
        if 'c' not in self.property_set:
            self.property_set['c'] = self.cx*self.cy
        return self.property_set['c']

    @property
    def wavelength(self):
        """中心波长"""
        return self.property_set.get_strictly('wavelength')
    
    @property
    def k(self):
        """波矢"""
        if 'k' not in self.property_set:
            self.property_set['k'] = 2*constants.pi/self.wavelength
        return self.property_set['k']

    @property
    def omega0x(self):
        """x方向束腰半径"""
        return self.property_set.get_strictly('omega0x')
    
    @property
    def omega0y(self):
        """y方向束腰半径"""
        return self.property_set.get_strictly('omega0y')
    
    @property
    def p0x(self):
        """x方向束腰位置"""
        return self.property_set.get_strictly('p0x')
    
    @property
    def p0y(self):
        """y方向束腰位置"""
        return self.property_set.get_strictly('p0y')
    
    @property
    def mx(self) -> int:
        """x方向Hermite-Gaussian光的模式"""
        return self.property_set.get_strictly('mx')
    
    @property
    def my(self) -> int:
        """y方向Hermite-Gaussian光的模式"""
        return self.property_set.get_strictly('my')

    @property
    def z0x(self):
        """x方向瑞利长度"""
        if 'z0x' not in self.property_set:
            self.property_set['z0x'] = self.__beams[0].z0
        return self.property_set['z0x']
    
    @property
    def z0y(self):
        """y方向瑞利长度"""
        if 'z0y' not in self.property_set:
            self.property_set['z0y'] = self.__beams[1].z0
        return self.property_set['z0y']
    
    @property
    def hmx(self):
        """x方向Hermite多项式"""
        if 'hmx' not in self.property_set:
            self.property_set['hmx'] = self.__beams[0].hm
        return self.property_set['hm']
    
    @property
    def hmy(self):
        """y方向Hermite多项式"""
        if 'hmy' not in self.property_set:
            self.property_set['hmy'] = self.__beams[1].hm
        return self.property_set['hmy']
    
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
        """x方向相位函数"""
        return self.__beams[0].phi_f(z)
    
    def phiy_f(self, z):
        """y方向相位函数"""
        return self.__beams[1].phi_f(z)
    
    def psix_f(self, z, x):
        """x方向Hermite-Gaussian模式"""
        return self.__beams[0].psi_f(z, x)
    
    def psiy_f(self, z, y):
        """x方向Hermite-Gaussian模式"""
        return self.__beams[1].psi_f(z, y)
    
    def u_f(self, z, x, y):
        """强度函数"""
        amplx, phasex = self.__beams[0].u_f(z, x)
        amply, phasey = self.__beams[1].u_f(z, y)
        return amplx*amply, phasex+phasey


class HermiteGaussBeam2D(NormalizedHermiteGaussBeam2D):
    name = 'HermiteGaussBeam2D'

    # 振幅, 波长, x方向束腰半径, y方向束腰半径, x方向束腰位置, y方向束腰位置, x方向模式数, y方向模式数
    modifiable_properties = ('A0', 'wavelength', 'omega0x', 'omega0y', 'p0x', 'p0y', 'mx', 'my')

    def __init__(self, A0, wavelength, omega0x, omega0y, p0x, p0y, mx, my, name='HermiteGaussBeam2D'):
        super().__init__(wavelength, omega0x, omega0y, p0x, p0y, mx, my)
        self.name = name

        # 振幅
        self.property_set.add_required('A0')
        self.property_set['A0'] = A0
    
    @property
    def A0(self):
        """振幅"""
        return self.property_set['A0']

    def A_f(self, z):
        """振幅函数"""
        A0 = self.A0
        A = super().A_f(z)
        return A0*A


class NormalizedGaussBeam2D(NormalizedHermiteGaussBeam2D):
    name = 'NormalizedGaussBeam2D'

    # 波长, x方向束腰半径, y方向束腰半径, x方向束腰位置, y方向束腰位置
    modifiable_properties = ('wavelength', 'omega0x', 'omega0y', 'p0x', 'p0y')

    def __init__(self, wavelength, omega0x, omega0y, p0x, p0y, name='NormalizedGaussBeam2D'):
        super().__init__(wavelength, omega0x, omega0y, p0x, p0y, mx=0, my=0)
        self.name = name


class GaussBeam2D(HermiteGaussBeam2D):
    name = 'HermiteGaussBeam2D'

    # 振幅, 波长, x方向束腰半径, y方向束腰半径, x方向束腰位置, y方向束腰位置
    modifiable_properties = ('A0', 'wavelength', 'omega0x', 'omega0y', 'p0x', 'p0y')

    def __init__(self, A0, wavelength, omega0x, omega0y, p0x, p0y, name='HermiteGaussBeam2D'):
        super().__init__(A0, wavelength, omega0x, omega0y, p0x, p0y, mx=0, my=0)
        self.name = name


class NormalizedSymmetricHermiteGaussBeam(NormalizedHermiteGaussBeam1D):
    name = 'NormalizedSymmetricHermiteGaussBeam'

    # 波长, 束腰半径, 束腰位置, 模式数
    modifiable_properties = ('wavelength', 'omega0', 'p0', 'm')

    def __init__(self, wavelength, omega0, p0, m, name='NormalizedSymmetricHermiteGaussBeam'):
        self.name = name

        self.property_set.PropertySet(NormalizedSymmetricHermiteGaussBeam.modifiable_properties)
        self.property_set['wavelength'] = wavelength
        self.property_set['omega0'] = omega0
        self.property_set['p0'] = p0
        self.property_set['m'] = m
    
    @property
    def c(self):
        """归一化因子"""
        if 'c' not in self.property_set:
            self.property_set['c'] = (super().c)**2
        return self.property_set['c']
    
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


class SymmetricHermiteGaussBeam(NormalizedSymmetricHermiteGaussBeam):
    name = 'SymmetricHermiteGaussBeam'

    # 振幅, 波长, 束腰半径, 束腰位置, 模式数
    modifiable_properties = ('A0', 'wavelength', 'omega0', 'p0', 'm')

    def __init__(self, A0, wavelength, omega0, p0, m, name='SymmetricHermiteGaussBeam'):
        super().__init__(wavelength, omega0, p0, m)
        self.name = name

        self.property_set.add_required('A0')
        self.property_set['A0'] = A0
    
    @property
    def A0(self):
        """振幅"""
        return self.property_set.get_strictly('A0')

    def A_f(self, z):
        """振幅函数"""
        A0 = self.A0
        A = super().A_f(z)
        return A0*A


class NormalizedSymmetricGaussBeam(NormalizedSymmetricHermiteGaussBeam):
    name = 'NormalizedSymmetricGaussBeam'

    # 波长, 束腰半径, 束腰位置
    modifiable_properties = ('wavelength', 'omega0', 'p0')

    def __init__(self, wavelength, omega0, p0, name='NormalizedSymmetricGaussBeam'):
        super().__init__(wavelength, omega0, p0, m=0)
        self.name = name


class SymmetricGaussBeam(SymmetricHermiteGaussBeam):
    name = 'SymmetricGaussBeam'

    # 振幅, 波长, 束腰半径, 束腰位置
    modifiable_properties = ('A0', 'wavelength', 'omega0', 'p0')

    def __init__(self, A0, wavelength, omega0, p0, name='SymmetricGaussBeam'):
        super().__init__(A0, wavelength, omega0, p0, m=0)
        self.name = name


#################################################################################
## TO DO


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

