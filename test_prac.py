import unittest
import python_prac

class TestFileExists(unittest.TestCase):

	def test_file(self):
		self.assertTrue(python_prac.fileExists('driveData.csv'), "File does not exist!")
		print("File exists!")


class testRandomSpeed(unittest.TestCase):				#checks input speed against one speed in test case ?? Might have understood this one wrong...

	def testSpeed(self):

		definedValue=10.0

		self.assertEqual(python_prac.returnSpeed(),definedValue, "Speed does not match!")
		
		print("Speed matches!")

if __name__ == '__main__':
	unittest.main()