import unittest
import autoMPG3
import requests

class testAutoMPG(unittest.TestCase):

    def test___eq__(self):
        yota = autoMPG3.autoMPG('toyota','T-100',1996,15)
        yota2 = autoMPG3.autoMPG('toyota','T-100',1996,15)
        self.assertEqual(autoMPG3.autoMPG.__eq__(yota,yota2),True) #check that equality is proven true when true
        yota3 = autoMPG3.autoMPG('toyota','T-100',1996,16)
        self.assertEqual(autoMPG3.autoMPG.__eq__(yota,yota3),False) #equality is false when to objects are not equal

    def test___lt__(self):
        yota = autoMPG3.autoMPG('toyota','T-100',1996,15)
        yota2 = autoMPG3.autoMPG('toyota','T-100',1996,15)
        self.assertEqual(autoMPG3.autoMPG.__lt__(yota,yota2),False) #test two objects that are equals
        yota3 = autoMPG3.autoMPG('toyota','T-100',1996,14)
        self.assertEqual(autoMPG3.autoMPG.__lt__(yota,yota3),False) #Check if mpg of first object is greater than second
        yota4 = autoMPG3.autoMPG('toyota','T-100',1995,15)
        self.assertEqual(autoMPG3.autoMPG.__lt__(yota,yota4),False) #Check if year of first object is greater than second
        yota5 = autoMPG3.autoMPG('toyota','T-200',1995,15)
        self.assertEqual(autoMPG3.autoMPG.__lt__(yota,yota5),False) #chekc if model of first object is greater than second
        yota6 = autoMPG3.autoMPG('subaru','T-100',1995,15)
        self.assertEqual(autoMPG3.autoMPG.__lt__(yota,yota6),False) #check if make of first object is greater than second
        yota7 = autoMPG3.autoMPG('toyota','T-100',1996,16)
        self.assertEqual(autoMPG3.autoMPG.__lt__(yota,yota7),True) #check case when first object is actually smaller
        other = ('toyota','T-100',1996,16)
        self.assertEqual(autoMPG3.autoMPG.__lt__(yota,other),NotImplemented) #confirms that both types must be the same

    def test___hash__(self):
        yota = autoMPG3.autoMPG('toyota','T-100',1996,15)
        yota6 = autoMPG3.autoMPG('subaru','T-100',1995,15)
        newYota = yota
        self.assertNotEqual(autoMPG3.autoMPG.__hash__(yota),autoMPG3.autoMPG.__hash__(yota6)) #check that a specific hash is accurate
        self.assertEqual(autoMPG3.autoMPG.__hash__(yota),autoMPG3.autoMPG.__hash__(newYota))

if __name__ == '__main__':
    unittest.main()
