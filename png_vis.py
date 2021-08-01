#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      admin-mint
#
# Created:     04/01/2017
# Copyright:   (c) admin-mint 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import binascii,tkinter
from tkinter import filedialog
from sys import exit



def main():
    pass

def comprobar_firma():
    archivo.seek(1)
    if archivo.read(3)!=b"PNG":
        print("Este archivo no es una imagen PNG")
        exit ()

def comprobar_crc (cadena): # Fumción para comprobar crc32 de una cadena hexademical
    cadena=binascii.unhexlify(bytes (cadena,"ascii"))
    crc=binascii.crc32(cadena)
    return crc

def sust_cadena (cadena): # Función para insertar la cadena modficada correcta
    #archivo= open("c:/Users/admin-mint/Documents/Vikingos/Ejemplos/unreal/PortablePython_3.2.5.1/00000635.png", "rb+")
    archivo.seek(12)
    cadena1= archivo.read(4)
    if cadena1 == (b"IHDR"):
        #posicion = archivo.tell()
        archivo.seek(12)
        archivo.write(binascii.unhexlify(bytes(cadena,"ascii")))
    else:
        print ("No es una imagen correcta")

    archivo.close()

if __name__ == '__main__':
    main()

    root = tkinter.Tk() #esto se hace solo para eliminar la ventanita de Tkinter
    root.withdraw() #ahora se cierra
    archivo=filedialog.askopenfilename()
    archivo=open (archivo, "r+b")
    comprobar_firma() # Comprobamos si tiene la firma correcta

    #Buscamos el crc bueno que viene en la imagen

    archivo.seek(29) # Indice del CRC  incorporado
    crc_bueno=archivo.read(4)

    crc_bueno=str(binascii.hexlify(crc_bueno))
    #crc_bueno=str (crc_bueno)
    crc_bueno=str.upper(crc_bueno)[2:-1]
    print ("crc bueno convertida a str : ",crc_bueno)
    #exit ()

    # Extraemos la cadena completa de 13 bytes a partir de IHDR

    archivo.seek(12)
    cadena=archivo.read(17)
    cadena=str(binascii.hexlify(cadena))
    cadena=str.upper(cadena)[2:-1]
    print ("Cadena hex desde IHDR para comprobar CRC : ", cadena)
    #exit()

    #cadena = input("Cadena Hex:")
    #crc = comprobar_crc(cadena)
    #print ('CRC en dec:', crc)
    #print ('CRC en hex: %08X' % crc)
    #crc_bueno = input ("CRC vÃ¡lido:")
    #print (cadena)

    # Inciamos la búsqueda por fuerza bruta del ancho y alto

    for w in range(2000): # maximo ancho de 2000
        for h in range (2000): # maximo alto de 2000
            #print (w,h)
            #print ("%08X" % w + "%08X" % h)
            #print (cadena[24:])
            cadena_mod=cadena[0:8] + "%08X" % w + "%08X" % h + cadena[24:]
            crc = "%08X" % comprobar_crc(cadena_mod)
            #print ("CRC resultante: ",crc)
            #print ("Cadena mod : ",cadena_mod)
            if crc==crc_bueno:
                print ("El ancho es :", w)
                print ("El alto es :",h)
                print ("La cadena completa a sustituir es :",cadena_mod)
                break
        if h != 1999:
            break

    print ("Ahora vamos a insertar la cadena encontrada")
    sust_cadena(cadena_mod)









