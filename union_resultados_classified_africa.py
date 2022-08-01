import arcpy, os, glob, shutil
from os import remove
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension ("Spatial")

# Poner classified o unclassified según la carpeta que va a procesar
carpeta = 'classified'
classify = '/' + carpeta + '/'


# fechas: modificar cada una de las fechas de los proyectos
fecha_africa = '2004_01_01_to_2022_04_07'
fecha_etiopia = '2004_01_01_to_2022_04_07'
print(" ")

print("Antes de correr este script, recuerda cambiar el nombre de la carpeta 'region'")
print("por '_region_africa'. Despues crear una carpeta con el nombre 'region'")
print(" ")
 
# Ruta del path
path = raw_input("ruta del path (T:\\GISDATA_terra\\outputs\\Africa\\" + fecha_africa + "\\TIFF\\GEOGRAPHIC\\WGS84\\decrease): ")

# Ruta de la nueva carpeta 'region'
print("Creando la carpeta 'región' con los nuevos datos")
if not os.path.exists(path + "//region"):
    os.mkdir(path + "//region")
print(" ")

print("Creando la carpeta 'classified' con los nuevos datos")
if not os.path.exists(path + "//region//" + carpeta):
    os.mkdir(path + "//region//" + carpeta)


# archivo de salida
print("Leyendo ruta de archivo final...")
output_africa = r"T://GISDATA_terra//outputs//Africa//" + fecha_africa + "//TIFF//GEOGRAPHIC//WGS84//decrease//region" + classify + "africa_decrease_" + fecha_africa + ".tif"


# archivos a unir
print("Leyendo archivos a unir...")
africa = r"T:/GISDATA_terra/outputs/Africa/" + fecha_africa + "/TIFF/GEOGRAPHIC/WGS84/decrease/_region_africa" + classify + "africa_decrease_" + fecha_africa + ".tif"
print(africa)
etiopia = r"T:/GISDATA_terra/outputs/sw_ethiopia/" + fecha_etiopia + "/TIFF/GEOGRAPHIC/WGS84/decrease/region" + classify + "sw_decrease_" + fecha_etiopia + ".tif" 
print(etiopia)
print(" ")
print(" ")


etiopia1 = ExtractByAttributes(etiopia, "VALUE <> 1")


africa2 = arcpy.Raster(africa)

# Variables de entorno
arcpy.env.snapRaster = africa2
arcpy.env.extent = africa2
arcpy.env.cellSize = africa2
arcpy.env.mask = africa2


# Union de archivos con Raster calculator
print("Uniendo el Etiopia a Africa...")
resultado0 = Con(IsNull(etiopia1), africa, etiopia1)
print("Guardando archivo...")
resultado0.save(output_africa)
print(" ")
print(" ")


raster_tiff = output_africa
print("convirtiendo a ascii...")
ascii_final = r"T://GISDATA_terra//outputs//Africa//" + fecha_africa + "//ASCII//decrease//region" + classify + "africa_decrease_" + fecha_africa + ".asc"
ascii_converter = arcpy.RasterToASCII_conversion(raster_tiff, ascii_final)
print("Proceso terminado")
