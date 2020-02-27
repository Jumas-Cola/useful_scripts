import random

class matrix:
	def __init__(self, rows):
		try:
			self.rows = rows
		except NameError:
			pass

	def __add__(self, other):
		if ((len(self.rows)==len(other.rows)) and (len(self.rows[0])==len(other.rows[0]))):
			result=[[self.rows[i][j]+other.rows[i][j] for j in range(len(self.rows[0]))] for i in range(len(self.rows))]
			return matrix(result)
		else:
			raise TypeError('The dimension of the operands does not match.')

	def __mul__(self, other):
		if (len(self.rows[0])==len(other.rows)):
			l = len(self.rows)
			m = len(other.rows)
			n = len(other.rows[0])
			result=[[sum([self.rows[i][r]*other.rows[r][j] for r in range(m)]) for j in range(n)] for i in range(l)]
			return matrix(result)
		else:
			raise TypeError('The number of columns of the first operand does not coincide with the number of lines of the second operand.')

	def __pow__(self, other):
		if (len(self.rows[0])==len(self.rows)):
			result = self
			l = len(self.rows)
			for count in range(other-1):
				result=matrix([[sum([result.rows[i][r]*self.rows[r][j] for r in range(l)]) for j in range(l)] for i in range(l)])
			return result
		else:
			raise TypeError('Non-square matrix.')

	def transp(self):
		result=[[self.rows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))]
		return matrix(result)

	def rand_matrix(count_rows,count_cols,mini,maxi):
		result=[[random.randrange(mini, maxi+1, 1) for j in range(count_cols)] for i in range(count_rows)]
		return matrix(result)

	def show(self):
		result='\n'.join([' '.join([str(j) for j in i]) for i in self.rows])
		print(result)



if __name__ == "__main__":
	A = matrix.rand_matrix(4,4,0,3)
	A.show()
	print()
	B = A**5
	B.show()


