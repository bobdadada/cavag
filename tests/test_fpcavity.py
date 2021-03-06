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

class Test_EqualAxisymmetricCavityStructure(unittest.TestCase):

    def test_constructor(self):
        roc, length = 300, 500
        g = 1 - length/roc
        
        eascs = EqualAxisymmetricCavityStructure(roc=roc, length=length)

        self.assertEqual(eascs.roc, roc)
        self.assertEqual(eascs.rocl, roc)
        self.assertEqual(eascs.rocr, roc)
        self.assertEqual(eascs.length, length)

        self.assertEqual(eascs.g, g)
        self.assertEqual(eascs.gl, g)
        self.assertEqual(eascs.gr, g)

        self.assertEqual(eascs.isStable(), True)
        self.assertEqual(eascs.isCritical(), False)

    def test_change_properties(self):
        roc, length = 300, 500
        
        eascs = EqualAxisymmetricCavityStructure(roc=roc, length=length)

        length, roc = 400, 300
        g = 1 - length/roc

        eascs.change_params(length=length, roc=roc)

        self.assertEqual(eascs.roc, roc)
        self.assertEqual(eascs.rocl, roc)
        self.assertEqual(eascs.rocr, roc)
        self.assertEqual(eascs.length, length)

        self.assertEqual(eascs.g, g)
        self.assertEqual(eascs.gl, g)
        self.assertEqual(eascs.gr, g)

        self.assertEqual(eascs.isStable(), True)
        self.assertEqual(eascs.isCritical(), False)

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

class Test_EqualAxisymmetricCavity(unittest.TestCase):

    def test_constructor(self):
        length, roc, rl, rr = 400, 300, 0.9, 0.8

        g = 1 - length/roc
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)
                
        easc = EqualAxisymmetricCavity(length=length, roc=roc, rl=rl, rr=rr)

        self.assertEqual(easc.rl, rl)
        self.assertEqual(easc.rr, rr)
        self.assertEqual(easc.length, length)

        self.assertEqual(easc.roc, roc)
        self.assertEqual(easc.rocl, roc)
        self.assertEqual(easc.rocr, roc)
        self.assertEqual(easc.length, length)

        self.assertEqual(easc.g, g)
        self.assertEqual(easc.gl, g)
        self.assertEqual(easc.gr, g)
        self.assertAlmostEqual(easc.kappa, kappa)
        self.assertAlmostEqual(easc.fsr, fsr)
        self.assertAlmostEqual(easc.finesse, finesse)
    
    def test_change_properties(self):
        length, roc, rl, rr = 400, 300, 0.9, 0.8
                
        easc = EqualAxisymmetricCavity(length=length, roc=roc, rl=rl, rr=rr)

        length, roc = 300, 400
        
        easc.change_params(length=length, roc=roc)

        g = 1 - length/roc
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)

        self.assertEqual(easc.rl, rl)
        self.assertEqual(easc.rr, rr)
        self.assertEqual(easc.length, length)

        self.assertEqual(easc.roc, roc)
        self.assertEqual(easc.rocl, roc)
        self.assertEqual(easc.rocr, roc)
        self.assertEqual(easc.length, length)

        self.assertEqual(easc.g, g)
        self.assertEqual(easc.gl, g)
        self.assertEqual(easc.gr, g)
        self.assertAlmostEqual(easc.kappa, kappa)
        self.assertAlmostEqual(easc.fsr, fsr)
        self.assertAlmostEqual(easc.finesse, finesse)

class Test_AxisymmetricCavityMode(unittest.TestCase):

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

        acm = AxisymmetricCavityMode(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, A0=A0)

        self.assertEqual(acm.length, length)
        self.assertEqual(acm.wavelength, wavelength)
        self.assertEqual(acm.rocl, rocl)
        self.assertEqual(acm.A0, A0)
        self.assertEqual(acm.nu, nu)

        self.assertEqual(acm.gl, gl)
        self.assertEqual(acm.gr, gr)
        self.assertEqual(acm.pl, pl)
        self.assertEqual(acm.pr, pr)
        self.assertEqual(acm.z0, z0)
        self.assertEqual(acm.p0, p0)
        self.assertEqual(acm.omega0, omega0)
        self.assertEqual(acm.omegaml, omegaml)
        self.assertEqual(acm.omegamr, omegamr)
        self.assertEqual(acm.V_mode, V_mode)
        self.assertEqual(acm.e, e)
    
    def test_change_properties(self):
        length, wavelength, rocl, rocr, A0 = 300, 9.8, 600, 400, 1
        
        acm = AxisymmetricCavityMode(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, A0=A0)
        length, wavelength, rocl, rocr, A0 = 450, 9.2, 500, 600, 2
        acm.change_params(length=length, wavelength=wavelength,
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

        self.assertEqual(acm.length, length)
        self.assertEqual(acm.wavelength, wavelength)
        self.assertEqual(acm.rocl, rocl)
        self.assertEqual(acm.A0, A0)
        self.assertEqual(acm.nu, nu)

        self.assertEqual(acm.gl, gl)
        self.assertEqual(acm.gr, gr)
        self.assertEqual(acm.pl, pl)
        self.assertEqual(acm.pr, pr)
        self.assertEqual(acm.z0, z0)
        self.assertEqual(acm.p0, p0)
        self.assertEqual(acm.omega0, omega0)
        self.assertEqual(acm.omegaml, omegaml)
        self.assertEqual(acm.omegamr, omegamr)
        self.assertEqual(acm.V_mode, V_mode)
        self.assertEqual(acm.e, e)

class Test_EqualAxisymmetricCavityMode(unittest.TestCase):
   
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

        eacm = EqualAxisymmetricCavityMode(length=length, wavelength=wavelength,
                roc=roc, A0=A0)

        self.assertEqual(eacm.length, length)
        self.assertEqual(eacm.wavelength, wavelength)
        self.assertEqual(eacm.roc, roc)
        self.assertEqual(eacm.rocl, rocl)
        self.assertEqual(eacm.A0, A0)
        self.assertEqual(eacm.nu, nu)

        self.assertEqual(eacm.g, g)
        self.assertEqual(eacm.gl, gl)
        self.assertEqual(eacm.gr, gr)
        self.assertEqual(eacm.pl, pl)
        self.assertEqual(eacm.pr, pr)
        self.assertEqual(eacm.z0, z0)
        self.assertEqual(eacm.p0, p0)
        self.assertEqual(eacm.omega0, omega0)
        self.assertEqual(eacm.omegaml, omegaml)
        self.assertEqual(eacm.omegamr, omegamr)
        self.assertEqual(eacm.V_mode, V_mode)
        self.assertEqual(eacm.e, e)
    
    def test_change_properties(self):
        length, wavelength, roc, A0 = 300, 9.8, 400, 1
        
        eacm = EqualAxisymmetricCavityMode(length=length, wavelength=wavelength,
                roc=roc, A0=A0)
        length, wavelength, roc, A0 = 400, 9.1, 300, 2
        eacm.change_params(length=length, wavelength=wavelength,
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

        self.assertEqual(eacm.length, length)
        self.assertEqual(eacm.wavelength, wavelength)
        self.assertEqual(eacm.roc, roc)
        self.assertEqual(eacm.rocl, rocl)
        self.assertEqual(eacm.A0, A0)
        self.assertEqual(eacm.nu, nu)

        self.assertEqual(eacm.g, g)
        self.assertEqual(eacm.gl, gl)
        self.assertEqual(eacm.gr, gr)
        self.assertEqual(eacm.pl, pl)
        self.assertEqual(eacm.pr, pr)
        self.assertEqual(eacm.z0, z0)
        self.assertEqual(eacm.p0, p0)
        self.assertEqual(eacm.omega0, omega0)
        self.assertEqual(eacm.omegaml, omegaml)
        self.assertEqual(eacm.omegamr, omegamr)
        self.assertEqual(eacm.V_mode, V_mode)
        self.assertEqual(eacm.e, e)

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

