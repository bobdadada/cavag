import unittest

import numpy as np
from scipy import constants
from cavag.fpcavity import *

class Test_CavityStructure(unittest.TestCase):

    def test_constructor(self):
        rocl, rocr, length = 300, 300, 400
        gl = 1 - length/rocl
        gr = 1 - length/rocr
        
        ascs = CavityStructure(rocl=rocl, rocr=rocr, length=length)
        
        self.assertEqual(ascs.rocl, rocl)
        self.assertEqual(ascs.rocr, rocr)
        self.assertEqual(ascs.length, length)

        self.assertEqual(ascs.gl, gl)
        self.assertEqual(ascs.gr, gr)

        self.assertEqual(ascs.isStable(), True)
        self.assertEqual(ascs.isCritical(), False)
        
    def test_change_properties(self):
        rocl, rocr, length = 300, 300, 400

        ascs = CavityStructure(rocl=rocl, rocr=rocr, length=length)

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

class Test_SymmetricCavityStructure(unittest.TestCase):

    def test_constructor(self):
        roc, length = 300, 500
        g = 1 - length/roc
        
        scs = SymmetricCavityStructure(roc=roc, length=length)

        self.assertEqual(scs.roc, roc)
        self.assertEqual(scs.rocl, roc)
        self.assertEqual(scs.rocr, roc)
        self.assertEqual(scs.length, length)

        self.assertEqual(scs.g, g)
        self.assertEqual(scs.gl, g)
        self.assertEqual(scs.gr, g)

        self.assertEqual(scs.isStable(), True)
        self.assertEqual(scs.isCritical(), False)

    def test_change_properties(self):
        roc, length = 300, 500
        
        scs = SymmetricCavityStructure(roc=roc, length=length)

        length, roc = 400, 300
        g = 1 - length/roc

        scs.change_params(length=length, roc=roc)

        self.assertEqual(scs.roc, roc)
        self.assertEqual(scs.rocl, roc)
        self.assertEqual(scs.rocr, roc)
        self.assertEqual(scs.length, length)

        self.assertEqual(scs.g, g)
        self.assertEqual(scs.gl, g)
        self.assertEqual(scs.gr, g)

        self.assertEqual(scs.isStable(), True)
        self.assertEqual(scs.isCritical(), False)

class Test_Cavity(unittest.TestCase):

    def test_constructor(self):
        length, rocl, rocr, rl, rr = 400, 300, 200, 0.9, 0.8

        gl = 1 - length/rocl
        gr = 1 - length/rocr
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)
                
        asc = Cavity(length=length, rocl=rocl, rocr=rocr, rl=rl, rr=rr)

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

        asc = Cavity(length=length, rocl=rocl, rocr=rocr, rl=rl, rr=rr)

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

class Test_SymmetricCavity(unittest.TestCase):

    def test_constructor(self):
        length, roc, rl, rr = 400, 300, 0.9, 0.8

        g = 1 - length/roc
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)
                
        sc = SymmetricCavity(length=length, roc=roc, rl=rl, rr=rr)

        self.assertEqual(sc.rl, rl)
        self.assertEqual(sc.rr, rr)
        self.assertEqual(sc.length, length)

        self.assertEqual(sc.roc, roc)
        self.assertEqual(sc.rocl, roc)
        self.assertEqual(sc.rocr, roc)
        self.assertEqual(sc.length, length)

        self.assertEqual(sc.g, g)
        self.assertEqual(sc.gl, g)
        self.assertEqual(sc.gr, g)
        self.assertAlmostEqual(sc.kappa, kappa)
        self.assertAlmostEqual(sc.fsr, fsr)
        self.assertAlmostEqual(sc.finesse, finesse)
    
    def test_change_properties(self):
        length, roc, rl, rr = 400, 300, 0.9, 0.8
                
        sc = SymmetricCavity(length=length, roc=roc, rl=rl, rr=rr)

        length, roc = 300, 400
        
        sc.change_params(length=length, roc=roc)

        g = 1 - length/roc
        kappa = constants.c*(2-rr-rl)/(4*length)
        fsr = 2*constants.pi*constants.c/(2*length)
        finesse = fsr/(2*kappa)

        self.assertEqual(sc.rl, rl)
        self.assertEqual(sc.rr, rr)
        self.assertEqual(sc.length, length)

        self.assertEqual(sc.roc, roc)
        self.assertEqual(sc.rocl, roc)
        self.assertEqual(sc.rocr, roc)
        self.assertEqual(sc.length, length)

        self.assertEqual(sc.g, g)
        self.assertEqual(sc.gl, g)
        self.assertEqual(sc.gr, g)
        self.assertAlmostEqual(sc.kappa, kappa)
        self.assertAlmostEqual(sc.fsr, fsr)
        self.assertAlmostEqual(sc.finesse, finesse)

class Test_CavityMode(unittest.TestCase):

    def test_constructor(self):
        length, wavelength, rocl, rocr, a0 = 300, 9.8, 600, 400, 1
        
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
        v_mode = length*omega0**2*constants.pi/4
        emax = np.sqrt(constants.h*nu/(2*constants.epsilon_0*v_mode))

        acm = CavityMode(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, a0=a0)

        self.assertEqual(acm.length, length)
        self.assertEqual(acm.wavelength, wavelength)
        self.assertEqual(acm.rocl, rocl)
        self.assertEqual(acm.a0, a0)
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
        self.assertEqual(acm.v_mode, v_mode)
        self.assertEqual(acm.emax, emax)
    
    def test_change_properties(self):
        length, wavelength, rocl, rocr, a0 = 300, 9.8, 600, 400, 1
        
        acm = CavityMode(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, a0=a0)
        length, wavelength, rocl, rocr, a0 = 450, 9.2, 500, 600, 2
        acm.change_params(length=length, wavelength=wavelength,
                rocl=rocl, rocr=rocr, a0=a0)
        
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
        v_mode = length*omega0**2*constants.pi/4
        emax = np.sqrt(constants.h*nu/(2*constants.epsilon_0*v_mode))

        self.assertEqual(acm.length, length)
        self.assertEqual(acm.wavelength, wavelength)
        self.assertEqual(acm.rocl, rocl)
        self.assertEqual(acm.a0, a0)
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
        self.assertEqual(acm.v_mode, v_mode)
        self.assertEqual(acm.emax, emax)

class Test_SymmetricCavityMode(unittest.TestCase):
   
    def test_constructor(self):
        length, wavelength, roc, a0 = 300, 9.8, 400, 1
        
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
        v_mode = length*omega0**2*constants.pi/4
        emax = np.sqrt(constants.h*nu/(2*constants.epsilon_0*v_mode))

        scm = SymmetricCavityMode(length=length, wavelength=wavelength,
                roc=roc, a0=a0)

        self.assertEqual(scm.length, length)
        self.assertEqual(scm.wavelength, wavelength)
        self.assertEqual(scm.roc, roc)
        self.assertEqual(scm.rocl, rocl)
        self.assertEqual(scm.a0, a0)
        self.assertEqual(scm.nu, nu)

        self.assertEqual(scm.g, g)
        self.assertEqual(scm.gl, gl)
        self.assertEqual(scm.gr, gr)
        self.assertEqual(scm.pl, pl)
        self.assertEqual(scm.pr, pr)
        self.assertEqual(scm.z0, z0)
        self.assertEqual(scm.p0, p0)
        self.assertEqual(scm.omega0, omega0)
        self.assertEqual(scm.omegaml, omegaml)
        self.assertEqual(scm.omegamr, omegamr)
        self.assertEqual(scm.v_mode, v_mode)
        self.assertEqual(scm.emax, emax)
    
    def test_change_properties(self):
        length, wavelength, roc, a0 = 300, 9.8, 400, 1
        
        scm = SymmetricCavityMode(length=length, wavelength=wavelength,
                roc=roc, a0=a0)
        length, wavelength, roc, a0 = 400, 9.1, 300, 2
        scm.change_params(length=length, wavelength=wavelength,
                roc=roc, a0=a0)

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
        v_mode = length*omega0**2*constants.pi/4
        emax = np.sqrt(constants.h*nu/(2*constants.epsilon_0*v_mode))        

        self.assertEqual(scm.length, length)
        self.assertEqual(scm.wavelength, wavelength)
        self.assertEqual(scm.roc, roc)
        self.assertEqual(scm.rocl, rocl)
        self.assertEqual(scm.a0, a0)
        self.assertEqual(scm.nu, nu)

        self.assertEqual(scm.g, g)
        self.assertEqual(scm.gl, gl)
        self.assertEqual(scm.gr, gr)
        self.assertEqual(scm.pl, pl)
        self.assertEqual(scm.pr, pr)
        self.assertEqual(scm.z0, z0)
        self.assertEqual(scm.p0, p0)
        self.assertEqual(scm.omega0, omega0)
        self.assertEqual(scm.omegaml, omegaml)
        self.assertEqual(scm.omegamr, omegamr)
        self.assertEqual(scm.v_mode, v_mode)
        self.assertEqual(scm.emax, emax)

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

