import unittest

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

        length = 400
        g = 1 - length/roc

        sascs.change_params(length=length)

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
        pass