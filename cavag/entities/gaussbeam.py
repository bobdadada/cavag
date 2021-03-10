import scipy as sp
from scipy import constants
from .misc import Position

__all__ = [
    'GaussBeam',
    'convert_through_mirror',
    'local2remote',
    'remote2local',
    'get_spot_info_after_deviation'
]

class GaussBeam(Position):
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

