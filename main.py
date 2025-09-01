import numpy as np
import matplotlib.pyplot as plt
import cmath
class reactance():
	def __init__(self,Z_c:complex):
		"""
		"""
		self.Z_c=Z_c
	def __add__(self,other):
		"""
		In group addition. Represents series reactance
		"""
		if isinstance(other,(int,float,complex)):
			# Just treat the value as instance of
			# reactange with Zc provided directly
			return reactance(self.Z_c+other)
		return reactance(self.Z_c+other.Z_c)
	def __mul__(self,other):
		if isinstance(other,(int,float)):
			"""
			Scalar multiplication
			# same meaning as multiple adds of the same thing
			"""
			return reactance(self.Z_c*other)
		"""
		In class multiplication ---represents parallel reactance
		"""
		return reactance(self.Z_c*other.Z_c/(self.Z_c+other.Z_c))
	def __str__(self):
		return f"reactance({self.Z_c})"
	def __eq__(self,other):
		"""Checks closeness, might use custom tolerance in future
		"""
		return cmath.isclose(self.Z_c, other.Z_c)
	def __abs__(self):
		return np.abs(self.Z_c)
	@property
	def real(self):
		return self.Z_c.real
	@property
	def imag(self):
		return self.Z_c.imag
	@property
	def mag(self):
		return np.sqrt(self.Z_c.imag**2+self.Z_c.real**2)
	@property
	def phase(self):
		return np.arctan(self.Z_c.imag/self.Z_c.real)

def mul_check_associativity():
	A=reactance(5+5j)
	B=reactance(-12j)
	C = reactance(4)
	assert (A*B)*C==A*(B*C), "not associative"
def add_check_associativity():
	A=reactance(5+5j)
	B=reactance(-12j)
	C = reactance(4)
	assert (A+B)+C==A+(B+C), "not associative"
if __name__ == '__main__':
	print(dir(complex))
	add_check_associativity()
	mul_check_associativity()

	f=np.linspace(0.1,3,1000)*1e6
	w=2*np.pi*f
	Cr1=1e-9
	alpha=20
	Cr2=alpha*Cr1
	Lp=10e-6
	Rp=1000
	Cb=100e-9
	Z_Cr1=reactance(1/(1j*w*Cr1))*0.5
	Z_Cr2=reactance(1/(1j*w*Cr2))
	Z_Cr=Z_Cr1+Z_Cr2
	Z_Lp=reactance(1j*w*Lp)
	Z_Rp=reactance(Rp+0j)
	Z_cb=reactance(1/(1j*1*w*Cb))
	Z_DUT=(Z_Rp*Z_Lp)

	f_reson=np.sqrt(1/(Lp*(Cr1*Cr2)/(Cr1+Cr2)))/(2*np.pi)
	print("Resonant frequency", f_reson/1e6)
	Zeq=(Z_Cr*Z_DUT)+Z_cb
	fig, ax1 = plt.subplots()
	ax1.plot(f, Zeq.mag, 'r', label='real')
	ax1.set_xlabel('Frequency (Hz)')
	ax1.set_ylabel('real', color='r')
	ax1.tick_params(axis='y', labelcolor='r')

	# Create a second y-axis for  Zphase vs f on right axis
	ax2 = ax1.twinx()
	ax2.plot(f,Zeq.phase , 'b', label='phase(rad/s)')
	ax2.set_ylabel('phase(rad)', color='b')
	ax2.tick_params(axis='y', labelcolor='b')
	# Add title and show plot
	plt.title('Magnitude and Phase plot')
	fig.tight_layout()

	plt.show()