import unittest

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

class Test_AxisymmetricCavityHerimiteGaussMode(unittest.TestCase):

    def test_constructor(self):
        pass