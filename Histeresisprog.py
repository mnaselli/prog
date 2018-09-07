#!/usr/bin/env python3
import csv
import numpy as np
import matplotlib.pyplot as plt

class Titulo:
	def __init__(self,nom,pes,fec):
		self.Nombre = nom
		self.Peso = pes
		self.Fecha = fec

class Datos:
	def __init__(self,camp,magne):
		self.Campo = camp
		self.Magnetizacion = magne

def Main():
	print ("Ingrese nombre del documento con los datos")
	entrada = input()

	with open( entrada, newline='') as ifile:
		reader = csv.reader(ifile)
		listaoriginal = [] 
		listamodificada = []
		fila = 0 #contador de filas
		cantmuestras = 0 #cantidad de muestras
		with open("salida.csv","w") as Salida:
			Salida.write('Muestra,Ms,Hc,Xinicial,Pend,Xpara \n')
			for row in reader:
				if row[0] == "AMO":
					cantmuestras = cantmuestras + 1

			ifile.seek(0)
			for row in reader:
				if fila == 0 :
					Firstline = Titulo(row[1],float(row[2]),row[3])
					listaoriginal = []
					listamodificada = []
				if fila >= 2 :
					nuevo = Datos(float(row[1]),float(row[3]))
					listaoriginal = nuevo
					print (nuevo.Magnetizacion)
					nuevo.Magnetizacion = nuevo.Magnetizacion * 0.001415
					print (nuevo.Magnetizacion)
					listamodificada.append(nuevo)
				fila = fila + 1
				if fila == 58 :
					fila = 0
					Calculardatos(listamodificada,Salida,Firstline)
			Salida.close()
	ifile.close()	


def Calculardatos(Listadat,Salida,Firstline):
	posmin = Minimoc(Listadat)
	Haltan = Pendiente(Listadat[(posmin - 5):posmin])	
	Haltap = Pendiente(Listadat[0:5])
	Halta = (Haltan + Haltap ) /2
	#print(Firstline.Nombre + ":" + str(Haltan) + " " + str(Haltap) + " " + str(Halta) + " " + str(len(Listadat)) + "\n")
	Correjida = []
	Correjida = Corregir(Listadat, Halta)
	Mag0d = Magnecero1(Correjida)
	Mag0a = Magnecero2(Correjida[Mag0d:])
	Mag0a = Mag0a + Mag0d
	X01 = Encontrarx0(Correjida,Mag0d)
	X02 = Encontrarx0(Correjida,Mag0a)
	X0 = (X01 + X02)/2
	Hpend = (Pendiente(Correjida[Mag0d - 2 : Mag0d + 2]) + Pendiente(Correjida[Mag0d - 2 : Mag0a + 2])) / 2
	Camp0d = Campocero1(Correjida)
	Camp0i = Campocero2(Correjida[Camp0d:])
	Camp0i = Camp0i + Camp0d
	Magcamp0 = (Tindep(Correjida[Camp0i - 2 : Camp0i + 2]) + Tindep(Correjida[Camp0d - 2 : Camp0d + 2])) / 2
	Salida.write(Firstline.Nombre + ',' + str(Magcamp0) + ',' + str(X0) + ',' + str(Hpend) + ',' + str(Halta) + '\n')
	Graficar(Correjida,Firstline)
	
def Minimoc(lis):
	cont = 0
	while cont < len(lis) and lis[cont].Campo > lis[cont +1].Campo :
		cont = cont +1
	return cont

def Encontrarx0(lis,mag0):
	valores = lis[(mag0 - 2):(mag0 + 2)]
	pend = Pendiente(valores)
	termino = Tindep(valores)
	res = (termino * -1) / pend
	return res


def Magnecero1(lis):
	cont = 0
	while lis[cont + 1].Magnetizacion > 0 :
		cont = cont +1
	return cont

def Magnecero2(lis):
	cont = 0
	while lis[cont + 1].Magnetizacion < 0 :
		cont = cont +1
	return cont


def Campocero1(lis):
	cont = 0
	while lis[cont + 1].Campo > 0 :
		cont = cont +1
	return cont

def Campocero2(lis):
	cont = 0
	while lis[cont + 1].Campo < 0 :
		cont = cont +1
	return cont





def Tindep(lis):
	Sumxy = 0
	cant = len(lis)
	cont = 0
	while cont < cant:
		Sumxy = Sumxy + lis[cont].Campo * lis[cont].Magnetizacion
		cont = cont +1
	Sumx = 0
	cont = 0
	while cont < cant:
		Sumx = Sumx + lis[cont].Campo
		cont = cont +1
	Sumy = 0
	cont = 0
	while cont < cant:
		Sumy = Sumy + lis[cont].Magnetizacion
		cont = cont +1
	Sumsqrx = 0
	cont = 0
	while cont < cant:
		Sumsqrx = Sumsqrx + lis[cont].Campo ** 2
		cont = cont +1

	res = ((Sumsqrx * Sumy) - (Sumx * Sumxy)) / ((cant * Sumsqrx) - Sumx ** 2)
	return res

def Corregir(Listadat, Halta):
	cont = 0
	Correjida = []
	while cont < len(Listadat) :
		Nuevo = Datos(Listadat[cont].Campo, Listadat[cont].Magnetizacion - (Halta * Listadat[cont].Campo))
		#print(str(Listadat[cont].Magnetizacion - (Halta * Listadat[cont].Campo)))
		Correjida.append(Nuevo)
		cont = cont +1
	return Correjida

def Pendiente(lis):
	Sumxy = 0
	cant = len(lis)
	cont = 0
	while cont < cant:
		Sumxy = Sumxy + lis[cont].Campo * lis[cont].Magnetizacion
		cont = cont +1
	Sumx = 0
	cont = 0
	while cont < cant:
		Sumx = Sumx + lis[cont].Campo
		cont = cont +1
	Sumy = 0
	cont = 0
	while cont < cant:
		Sumy = Sumy + lis[cont].Magnetizacion
		cont = cont +1
	Sumsqrx = 0
	cont = 0
	while cont < cant:
		Sumsqrx = Sumsqrx + lis[cont].Campo ** 2
		cont = cont +1
#	print(" sumax: " + str(Sumx) + " sumay: " + str(Sumy) + " sumaxy: " + str(Sumxy) + " sumax2: " + str(Sumsqrx) + " cantidad: " + str(cant +1))
	res = (((cant) * Sumxy) - (Sumx * Sumy))/(((cant) * Sumsqrx) - Sumx * Sumx)
	return res

def Graficar(lis,Firstline):
	X = []
	Y = []
	cont = 0
	while cont < len(lis):
		X.append(float(lis[cont].Campo))
		Y.append(float(lis[cont].Magnetizacion))
		cont = cont + 1
	plt.plot(X, Y)
	plt.axhline(0, color='black')
	plt.axvline(0, color='black')
	plt.savefig(Firstline.Nombre + ".png")
	plt.close()

Main()