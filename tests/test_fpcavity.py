import unittest

import numpy as np
from scipy import constants
from cavag.fpcavity import *

class Test_AxisymmetricCavityStructure(unittest.TestCase):

    def test_constructor(self):
        rocl, rocr, length = 300, 300, 400
        gl = 1 - length/rocl
        gr = 1 - length/rocr
        
        ascs = AxisymmetricCavityStructure(rocl=rocl, rocr=rocr, length=length)
        
        self.assertEqual(ascs.rocl, rocl)
        self.assertEqual(ascs.rocr, rocr)
        self.assertEqual(ascs.length, length)

        self.assertEqual(ascs.gl, gl)
        self.assertEqual(ascs.gr, gr)

        self.assertEqual(ascs.isStable(), True)
        self.assertEqual(ascs.isCritical(), False)
        
    def test_change_properties(self):
        rocl, rocr, length = 300, 300, 400

        ascs = AxisymmetricCavityStructure(rocl=rocl, rocr=rocr, length=length)

        rocl = 200 
        gl = 1 - length/rocl
        gr = 1 - length/rocr

        ascs.change_params(rocl=rocl, rocr=rocr, length=length)

        self.assertEqual(ascs.rocl, rocl)
        self.assertEqual(ascs.rocr, rocr)
        self.assertEqual(ascs.length, length)

        self.assertEqual(ascs.gl, gl)
        self.assertEqual(ascs.gr, gr)

        self.assertEqual(ascs.isStable(), True)
        self.assertEqual(ascs.isCritical(), False)

class Test_SymmetricAxisymmetricCavityStructure(unittest.TestCase):

    def test_constructor(self):
        roc, length = 300, 500
        g = 1 - length/roc
        
        sascs = SymmetricAxisymmetricCavityStructure(roc=roc, length=length)

        self.assertEqual(sascs.roc, roc)
        self.assertEqual(sascs.rocl, roc)
        self.assertEqual(sascs.rocr, roc)
        self.assertEqual(sascs.length, length)

        self.assertEqual(sascs.g, g)
        self.assertEqual(sascs.gl, g)
        self.assertEqual(sascs.gr, g)

        self.assertEqual(sascs.isStable(), True)
        self.assertEqual(sascs.isCritical(), False)

    def test_change_properties(self):
        roc, length = 300, 500
        
        sascs = SymmetricAxisymmetricCavityStructure(roc=roc, length=length)

        length, roc = 400, 300
        g = 1 - length/roc

        sascs.change_params(length=length, roc=roc)

        self.assertEqual(sascs.roc, roc)
        self.assertEqual(sascs.rocl, roc)
        self.assertEqual(sascs.rocr, roc)
        self.assertEqual(sascs.length, length)

        self.assertEqual(sascs.g, g)
        self.assertEqual(sascs.gl, g)
        self.assertEqual(sascs.gr, g)

        self.assertEqual(sascs.isStable(), True)
        self.assertEqual(sascs.isCritical(), False)

class Test_AxisymmetricCavity(unittest.TestCase):

    def test_constructor(self):
        length, rocl, rocr, rl, rr = 400, 300, 200, 0.9, 0.8

        gl = 1 - length/rocl
        gr = 1 - length/rocr
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)
                
        asc = AxisymmetricCavity(length=length, rocl=rocl, rocr=rocr, rl=rl, rr=rr)

        self.assertEqual(asc.rl, rl)
        self.assertEqual(asc.rr, rr)
        self.assertEqual(asc.length, length)

        self.assertEqual(asc.rocl, rocl)
        self.assertEqual(asc.rocr, rocr)
        self.assertEqual(asc.length, length)

        self.assertEqual(asc.gl, gl)
        self.assertEqual(asc.gr, gr)
        self.assertAlmostEqual(asc.kappa, kappa)
        self.assertAlmostEqual(asc.fsr, fsr)
        self.assertAlmostEqual(asc.finesse, finesse)
    
    def test_change_properties(self):
        length, rocl, rocr, rl, rr = 400, 300, 200, 0.9, 0.8

        asc = AxisymmetricCavity(length=length, rocl=rocl, rocr=rocr, rl=rl, rr=rr)

        length, rocr = 300, 300

        asc.change_params(length=length, rocr=rocr)

        gl = 1 - length/rocl
        gr = 1 - length/rocr
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)

        self.assertEqual(asc.rl, rl)
        self.assertEqual(asc.rr, rr)
        self.assertEqual(asc.length, length)

        self.assertEqual(asc.rocl, rocl)
        self.assertEqual(asc.rocr, rocr)
        self.assertEqual(asc.length, length)

        self.assertEqual(asc.gl, gl)
        self.assertEqual(asc.gr, gr)
        self.assertAlmostEqual(asc.kappa, kappa)
        self.assertAlmostEqual(asc.fsr, fsr)
        self.assertAlmostEqual(asc.finesse, finesse)

class Test_SymmetricAxisymmetricCavity(unittest.TestCase):

    def test_constructor(self):
        length, roc, rl, rr = 400, 300, 0.9, 0.8

        g = 1 - length/roc
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)
                
        sasc = SymmetricAxisymmetricCavity(length=length, roc=roc, rl=rl, rr=rr)

        self.assertEqual(sasc.rl, rl)
        self.assertEqual(sasc.rr, rr)
        self.assertEqual(sasc.length, length)

        self.assertEqual(sasc.roc, roc)
        self.assertEqual(sasc.rocl, roc)
        self.assertEqual(sasc.rocr, roc)
        self.assertEqual(sasc.length, length)

        self.assertEqual(sasc.g, g)
        self.assertEqual(sasc.gl, g)
        self.assertEqual(sasc.gr, g)
        self.assertAlmostEqual(sasc.kappa, kappa)
        self.assertAlmostEqual(sasc.fsr, fsr)
        self.assertAlmostEqual(sasc.finesse, finesse)
    
    def test_change_properties(self):
        length, roc, rl, rr = 400, 300, 0.9, 0.8
                
        sasc = SymmetricAxisymmetricCavity(length=length, roc=roc, rl=rl, rr=rr)

        length, roc = 300, 400
        
        sasc.change_params(length=length, roc=roc)

        g = 1 - length/roc
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)

        self.assertEqual(sasc.rl, rl)
        self.assertEqual(sasc.rr, rr)
        self.assertEqual(sasc.length, length)

        self.assertEqual(sasc.roc, roc)
        self.assertEqual(sasc.rocl, roc)
        self.assertEqual(sasc.rocr, roc)
        self.assertEqual(sasc.length, length)

        self.assertEqual(sasc.g, g)
        self.assertEqual(sasc.gl, g)
        self.assertEqual(sasc.gr, g)
        self.assertAlmostEqual(sasc.kappa, kappa)
        self.assertAlmostEqual(sasc.fsr, fsr)
        self.assertAlmostEqual(sasc.finesse, finesse)

class Test_AxisymmetricCavityGaussMode(unittest.TestCase):

    def test_constructor(self):
        length, wavelength, rocl, rocr, A0 = 300, 9.8, 600, 400, 1
        
        nu = constants.c/wavelength
        gl = 1-length/rocl
        gr = 1-length/rocr
        z0 = np.sqrt(gl*gr*(1-gl*gr)/(gl+gr-2*gl*gr)**2)*length
        omega0 = np.sqrt(wavelength*z0/constants.pi)
        pl = gr*(1-gl)/(gl+gr-2*gl*gr)*length
        pr = gl*(1-gr)/(gl+gr-2*gl*gr)*length
        p0 = (pl-pr)/2
        omegaml = omega0*np.sqrt(1+(pl/z0)**2)
        omegamr = omega0*np.sqrt(1+(pr/z0)**2)
        V_mode = length*omega0**2*constants.pi/4
        e = np.sqrt(constants.h*nu/(2*constants.epsilon_0*V_mode))

        acgm = AxisymmetricCavityGaussMode(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, A0=A0)

        self.assertEqual(acgm.length, length)
        self.assertEqual(acgm.wavelength, wavelength)
        self.assertEqual(acgm.rocl, rocl)
        self.assertEqual(acgm.A0, A0)
        self.assertEqual(acgm.nu, nu)

        self.assertEqual(acgm.gl, gl)
        self.assertEqual(acgm.gr, gr)
        self.assertEqual(acgm.pl, pl)
        self.assertEqual(acgm.pr, pr)
        self.assertEqual(acgm.z0, z0)
        self.assertEqual(acgm.p0, p0)
        self.assertEqual(acgm.omega0, omega0)
        self.assertEqual(acgm.omegaml, omegaml)
        self.assertEqual(acgm.omegamr, omegamr)
        self.assertEqual(acgm.V_mode, V_mode)
        self.assertEqual(acgm.e, e)
    
    def test_change_properties(self):
        length, wavelength, rocl, rocr, A0 = 300, 9.8, 600, 400, 1
        
        acgm = AxisymmetricCavityGaussMode(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, A0=A0)
        length, wavelength, rocl, rocr, A0 = 450, 9.2, 500, 600, 2
        acgm.change_params(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, A0=A0)
        
        nu = constants.c/wavelength
        gl = 1-length/rocl
        gr = 1-length/rocr
        z0 = np.sqrt(gl*gr*(1-gl*gr)/(gl+gr-2*gl*gr)**2)*length
        omega0 = np.sqrt(wavelength*z0/constants.pi)
        pl = gr*(1-gl)/(gl+gr-2*gl*gr)*length
        pr = gl*(1-gr)/(gl+gr-2*gl*gr)*length
        p0 = (pl-pr)/2
        omegaml = omega0*np.sqrt(1+(pl/z0)**2)
        omegamr = omega0*np.sqrt(1+(pr/z0)**2)
        V_mode = length*omega0**2*constants.pi/4
        e = np.sqrt(constants.h*nu/(2*constants.epsilon_0*V_mode))

        self.assertEqual(acgm.length, length)
        self.assertEqual(acgm.wavelength, wavelength)
        self.assertEqual(acgm.rocl, rocl)
        self.assertEqual(acgm.A0, A0)
        self.assertEqual(acgm.nu, nu)

        self.assertEqual(acgm.gl, gl)
        self.assertEqual(acgm.gr, gr)
        self.assertEqual(acgm.pl, pl)
        self.assertEqual(acgm.pr, pr)
        self.assertEqual(acgm.z0, z0)
        self.assertEqual(acgm.p0, p0)
        self.assertEqual(acgm.omega0, omega0)
        self.assertEqual(acgm.omegaml, omegaml)
        self.assertEqual(acgm.omegamr, omegamr)
        self.assertEqual(acgm.V_mode, V_mode)
        self.assertEqual(acgm.e, e)

class Test_SymmetricAxisymmetricCavityGaussMode(unittest.TestCase):
   
    def test_constructor(self):
        length, wavelength, roc, A0 = 300, 9.8, 400, 1
        
        nu = constants.c/wavelength
        g = 1-length/roc
        gl = g
        gr = g
        rocl = roc
        rocr = roc
        z0 = np.sqrt(gl*gr*(1-gl*gr)/(gl+gr-2*gl*gr)**2)*length
        omega0 = np.sqrt(wavelength*z0/constants.pi)
        pl = gr*(1-gl)/(gl+gr-2*gl*gr)*length
        pr = gl*(1-gr)/(gl+gr-2*gl*gr)*length
        p0 = (pl-pr)/2
        omegaml = omega0*np.sqrt(1+(pl/z0)**2)
        omegamr = omega0*np.sqrt(1+(pr/z0)**2)
        V_mode = length*omega0**2*constants.pi/4
        e = np.sqrt(constants.h*nu/(2*constants.epsilon_0*V_mode))

        sacgm = SymmetricAxisymmetricCavityGaussMode(length=length, wavelength=wavelength,
                roc=roc, A0=A0)

        self.assertEqual(sacgm.length, length)
        self.assertEqual(sacgm.wavelength, wavelength)
        self.assertEqual(sacgm.roc, roc)
        self.assertEqual(sacgm.rocl, rocl)
        self.assertEqual(sacgm.A0, A0)
        self.assertEqual(sacgm.nu, nu)

        self.assertEqual(sacgm.g, g)
        self.assertEqual(sacgm.gl, gl)
        self.assertEqual(sacgm.gr, gr)
        self.assertEqual(sacgm.pl, pl)
        self.assertEqual(sacgm.pr, pr)
        self.assertEqual(sacgm.z0, z0)
        self.assertEqual(sacgm.p0, p0)
        self.assertEqual(sacgm.omega0, omega0)
        self.assertEqual(sacgm.omegaml, omegaml)
        self.assertEqual(sacgm.omegamr, omegamr)
        self.assertEqual(sacgm.V_mode, V_mode)
        self.assertEqual(sacgm.e, e)
    
    def test_change_properties(self):
        length, wavelength, roc, A0 = 300, 9.8, 400, 1
        
        sacgm = SymmetricAxisymmetricCavityGaussMode(length=length, wavelength=wavelength,
                roc=roc, A0=A0)
        length, wavelength, roc, A0 = 400, 9.1, 300, 2
        sacgm.change_params(length=length, wavelength=wavelength,
                roc=roc, A0=A0)

        nu = constants.c/wavelength
        g = 1-length/roc
        gl = g
        gr = g
        rocl = roc
        rocr = roc
        z0 = np.sqrt(gl*gr*(1-gl*gr)/(gl+gr-2*gl*gr)**2)*length
        omega0 = np.sqrt(wavelength*z0/constants.pi)
        pl = gr*(1-gl)/(gl+gr-2*gl*gr)*length
        pr = gl*(1-gr)/(gl+gr-2*gl*gr)*length
        p0 = (pl-pr)/2
        omegaml = omega0*np.sqrt(1+(pl/z0)**2)
        omegamr = omega0*np.sqrt(1+(pr/z0)**2)
        V_mode = length*omega0**2*constants.pi/4
        e = np.sqrt(constants.h*nu/(2*constants.epsilon_0*V_mode))        

        self.assertEqual(sacgm.length, length)
        self.assertEqual(sacgm.wavelength, wavelength)
        self.assertEqual(sacgm.roc, roc)
        self.assertEqual(sacgm.rocl, rocl)
        self.assertEqual(sacgm.A0, A0)
        self.assertEqual(sacgm.nu, nu)

        self.assertEqual(sacgm.g, g)
        self.assertEqual(sacgm.gl, gl)
        self.assertEqual(sacgm.gr, gr)
        self.assertEqual(sacgm.pl, pl)
        self.assertEqual(sacgm.pr, pr)
        self.assertEqual(sacgm.z0, z0)
        self.assertEqual(sacgm.p0, p0)
        self.assertEqual(sacgm.omega0, omega0)
        self.assertEqual(sacgm.omegaml, omegaml)
        self.assertEqual(sacgm.omegamr, omegamr)
        self.assertEqual(sacgm.V_mode, V_mode)
        self.assertEqual(sacgm.e, e)

class Test_functions(unittest.TestCase):

    def test_judge_cavity_type(self):
        r1, r2 = judge_cavity_type(300, 200, 300)
        self.assertEqual(r1, True)
        self.assertEqual(r2, True)

        r1, r2 = judge_cavity_type(300, 200, 200)
        self.assertEqual(r1, True)
        self.assertEqual(r2, False)

        r1, r2 = judge_cavity_type(900, 400, 400)
        self.assertEqual(r1, False)
        self.assertEqual(r2, False)
    
    def test_calculate_loss_clipping(self):
        d, omegam = 200, 2
        cl = np.exp(-2*(d/2)**2/omegam**2)
        self.assertEqual(calculate_loss_clipping(d, omegam), cl)
    
    def test_calculate_loss_scattering(self):
        sigmasc, wavelength = 0.2, 980
        sl = (4*constants.pi*sigmasc/wavelength)**2
        self.assertEqual(calculate_loss_scattering(sigmasc, wavelength), sl)

