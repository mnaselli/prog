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
			for row in reader
				if fila == 0
					Firstline = Titulo(row[1],float(row[2]),row[3])
					listaoriginal = []
					listamodificada = []
				if fila >= 2
					nuevo = Datos[float(row[1]),float(row[3])]
					listaoriginal = nuevo
					nuevo.Magnetizacion = nuevo.Magnetizacion * 0.001415
					listamodificada.append(nuevo)
				fila = fila + 1
				if fila == 58
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