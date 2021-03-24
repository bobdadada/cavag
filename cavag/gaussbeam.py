import numpy as np
from scipy import constants
from scipy import special
from .misc import Wavelength

__all__ = [
    'NormalizedHermiteGaussBeam1D', 'HermiteGaussBeam1D',
    'NormalizedGaussBeam1D', 'GaussBeam1D',
    'NormalizedHermiteGaussBeam2D', 'HermiteGaussBeam2D',
    'NormalizedGaussBeam2D', 'GaussBeam2D',
    'NormalizedSymmetricHermiteGaussBeam', 'SymmetricHermiteGaussBeam',
    'NormalizedSymmetricGaussBeam', 'SymmetricGaussBeam'
]


class NormalizedHermiteGaussBeam1D(Wavelength):
    name = 'NormalizedHermiteGaussBeam1D'

    # 波长, 束腰位置, 束腰半径, 模式数
    modifiable_properties = ('wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='NormalizedHermiteGaussBeam1D', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(NormalizedHermiteGaussBeam1D.modifiable_properties)

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
        return self.get_property('theta', lambda:np.arctan(self.wavelength/(constants.pi*self.omega0)))
    
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


class NormalizedHermiteGaussBeam2D(Wavelength):
    name = 'NormalizedHermiteGaussBeam2D'

    # 波长, 束腰位置, x方向束腰半径, y方向束腰半径, x方向束腰位置, x方向模式数, y方向模式数
    modifiable_properties = ('wavelength', 'p0', 'omega0x', 'omega0y', 'mx', 'my')

    def __init__(self, name='NormalizedHermiteGaussBeam2D', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(NormalizedHermiteGaussBeam2D.modifiable_properties)

        for prop in NormalizedHermiteGaussBeam2D.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)

        __kwarg_beams = ({
            'wavelength': kwargs.get('wavelength', None),
            'p0': kwargs.get('p0', None),
            'omega0': kwargs.get('omega0x', None),
            'm': kwargs.get('mx', None),
        },{
            'wavelength': kwargs.get('wavelength', None),
            'p0': kwargs.get('p0', None),
            'omega0': kwargs.get('omega0y', None),
            'm': kwargs.get('my', None),
        })

        self.__beams = (
            NormalizedHermiteGaussBeam1D(name='x-direction', **(__kwarg_beams[0])),
            NormalizedHermiteGaussBeam1D(namm='y-direction', **(__kwarg_beams[1])),
        )
    
    def change_params(self, _filter=True, **kwargs):
        super().change_params(_filter=_filter, **kwargs)

        if _filter:
            kwargs = self.filter_properties(kwargs)

        self.update_propset(**kwargs)

        xkw, ykw = {}, {}
        for k, v in kwargs.items():
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


class HermiteGaussBeam2D(NormalizedHermiteGaussBeam2D):
    name = 'HermiteGaussBeam2D'

    # 振幅, 波长, 束腰位置, x方向束腰半径, y方向束腰半径, x方向模式数, y方向模式数
    modifiable_properties = ('A0', 'wavelength', 'p0', 'omega0x', 'omega0y', 'mx', 'my')

    def __init__(self, name='HermiteGaussBeam2D', **kwargs):
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


class NormalizedGaussBeam2D(NormalizedHermiteGaussBeam2D):
    name = 'NormalizedGaussBeam2D'

    modifiable_properties = ('wavelength', 'p0', 'omega0x', 'omega0y')

    def __init__(self, name='NormalizedGaussBeam2D', **kwargs):
        kwargs.update(mx=0, my=0)

        super().__init__(**kwargs)
        self.name = name


class GaussBeam2D(HermiteGaussBeam2D):
    name = 'HermiteGaussBeam2D'

    modifiable_properties = ('A0', 'wavelength', 'p0', 'omega0x', 'omega0y')

    def __init__(self, name='HermiteGaussBeam2D', **kwargs):
        kwargs.update(mx=0, my=0)

        super().__init__(**kwargs)
        self.name = name


class NormalizedSymmetricHermiteGaussBeam(NormalizedHermiteGaussBeam1D):
    name = 'NormalizedSymmetricHermiteGaussBeam'

    # 波长, 束腰半径, 束腰位置, 模式数
    modifiable_properties = ('wavelength', 'p0', 'omega0', 'm')

    def __init__(self, name='NormalizedSymmetricHermiteGaussBeam', **kwargs):
        super().__init__(**kwargs)
        self.name = name

        self.property_set.add_required(NormalizedSymmetricHermiteGaussBeam.modifiable_properties)

        for prop in NormalizedSymmetricHermiteGaussBeam.modifiable_properties:
            self.property_set[prop] = kwargs.get(prop, None)
    
    @property
    def c(self):
        """总归一化因子"""
        return self.get_property('c', lambda: (super(NormalizedSymmetricHermiteGaussBeam, self).c)**2)
    
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

    modifiable_properties = ('A0', 'p0', 'wavelength', 'omega0', 'm')

    def __init__(self, name='SymmetricHermiteGaussBeam', **kwargs):
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


class NormalizedSymmetricGaussBeam(NormalizedSymmetricHermiteGaussBeam):
    name = 'NormalizedSymmetricGaussBeam'

    modifiable_properties = ('wavelength', 'p0', 'omega0')

    def __init__(self, name='NormalizedSymmetricGaussBeam', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
        self.name = name


class SymmetricGaussBeam(SymmetricHermiteGaussBeam):
    name = 'SymmetricGaussBeam'

    modifiable_properties = ('A0', 'wavelength', 'p0', 'omega0')

    def __init__(self, name='SymmetricGaussBeam', **kwargs):
        kwargs.update(m=0)

        super().__init__(**kwargs)
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
    omega = omega0 * np.sqrt(1 + (s / zr) ** 2)
    R = s * (1 + (zr / s) ** 2)
    return omega, R


def remote2local(omega, R, wavelength):
    zrp = constants.pi * omega ** 2 / wavelength
    omega0 = omega / np.sqrt(1 + (zrp / R) ** 2)
    s = R / (1 + (R / zrp) ** 2)
    return omega0, s


def get_spot_info_after_deviation(beam, z):
    zr = constants.pi * beam.omega0 ** 2 / beam.wavelength
    R = z * (1 + (zr / z) ** 2)
    omega = beam.omega0 * np.sqrt(1 + (z / zr) ** 2)
    A = beam.A0 * beam.omega0 / omega
    return omega, R, A

