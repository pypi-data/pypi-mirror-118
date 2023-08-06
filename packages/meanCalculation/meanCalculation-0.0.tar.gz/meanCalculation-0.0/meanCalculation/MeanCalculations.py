import math
from .AvgCalculation import MeanCalc

class CalcMean(MeanCalc):

	def __init__(self):
		Mean.__init__(self)


	def calculate_mean(self):
		"""Function to calculate the mean of the data set.

		Args:
			None

		Returns:
			float: mean of the data set

		"""

		avg = 1.0 * sum(self.data) / len(self.data)

		self.mean = avg

		return self.mean


