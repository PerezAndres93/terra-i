import arcpy, os, glob, shutil
from os import remove
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension ("Spatial")

# Poner classified o unclassified según la carpeta que va a procesar
carpeta = 'unclassified'
classify = '/' + carpeta + '/'


# fechas: modificar cada una de las fechas de los proyectos
fecha_lat = '2004_01_01_to_2022_04_07'
fecha_salvador = '2004_01_01_to_2022_04_07'
fecha_ahuachapan = '2004_01_01_to_2022_04_07'
fecha_valle = '2004_01_01_to_2022_04_07'
fecha_honduras = '2004_01_01_to_2022_04_07'
fecha_peru = '2004_01_01_to_2022_04_07'


print("Antes de correr este script, recuerda cambiar el nombre de la carpeta 'region'")
print("por '_region_latin'. Despues crear una carpeta con el nombre 'region'.")
print("Tambien, debe renombrar el archivo en formato ascii.gz que se encuentra en")
print("las carpetas classified y unclassified. T:\GISDATA_terra\outputs\Latin\2004_01_01_to_2022_02_02\ASCII\decrease\region")
print("cuando esto termine, comprima el archivo nuevo a formato gz y borre el anterior")
 

# Ruta del path
path = raw_input("ruta del path (T:\\GISDATA_terra\\outputs\\Latin\\" + fecha_lat + "\\TIFF\\GEOGRAPHIC\\WGS84\\decrease): ")

# Ruta de la nueva carpeta 'region'
print("Creando la carpeta 'región' con los nuevos datos")
if not os.path.exists(path + "//region"):
    os.mkdir(path + "//region")
print(" ")

print("Creando la carpeta 'unclassified' con los nuevos datos")
if not os.path.exists(path + "//region//" + carpeta):
    os.mkdir(path + "//region//" + carpeta)


# archivo de salida
print("Leyendo ruta de archivo final...")
latin_elsalvador = r"T://GISDATA_terra//outputs//Latin//" + fecha_salvador + "//TIFF//GEOGRAPHIC//WGS84//decrease//region" + classify + "latin_elsalvador_" + fecha_salvador + ".tif"
latin_elsalvador_ahuachapan = r"T://GISDATA_terra//outputs//Latin//" + fecha_lat + "//TIFF//GEOGRAPHIC//WGS84//decrease//region" + classify + "latin_elsalvador_ahuachapan_" + fecha_lat + ".tif"
latin_elsalvador_ahuachapan_valle = r"T://GISDATA_terra//outputs//Latin//" + fecha_lat + "//TIFF//GEOGRAPHIC//WGS84//decrease//region" + classify + "latin_elsalvador_ahuachapan_valle_" + fecha_lat + ".tif"
latin_elsalvador_ahuachapan_valle_honduras = r"T://GISDATA_terra//outputs//Latin//" + fecha_lat + "//TIFF//GEOGRAPHIC//WGS84//decrease//region" + classify + "latin_elsalvador_ahuachapan_valle_honduras_" + fecha_lat + ".tif"
output_latin = r"T://GISDATA_terra//outputs//Latin//" + fecha_lat + "//TIFF//GEOGRAPHIC//WGS84//decrease//region" + classify + "latin_decrease_" + fecha_lat + ".tif"


# archivos a unir
print("Leyendo archivos a unir...")
latin = r"T:/GISDATA_terra/outputs/Latin/" + fecha_lat + "/TIFF/GEOGRAPHIC/WGS84/decrease/_region_latin" + classify + "latin_decrease_" + fecha_lat + ".tif"
print(latin)
elsalvador = r"T:/GISDATA_terra/outputs/el_salvador/" + fecha_salvador + "/TIFF/GEOGRAPHIC/WGS84/decrease/region/" + classify + "elsalvador_decrease_" + fecha_salvador + ".tif"
print(elsalvador)
ahuachapan = r"T:/GISDATA_terra/outputs/ahuachapan/" + fecha_ahuachapan + "/TIFF/GEOGRAPHIC/WGS84/decrease/region" + classify + "ahuachapan_decrease_" + fecha_ahuachapan + ".tif"
print(ahuachapan)
valle = r"T:/GISDATA_terra/outputs/CVC/" + fecha_valle + "/TIFF/GEOGRAPHIC/WGS84/decrease/region" + classify + "valle_decrease_" + fecha_valle + ".tif"
print(valle)
honduras = r"T:/GISDATA_terra/outputs/HONDURAS/" + fecha_honduras + "/TIFF/GEOGRAPHIC/WGS84/decrease/region" + classify + "honduras_decrease_" + fecha_honduras + ".tif"
print(honduras)
peru = r"T:/GISDATA_terra/outputs/Peru/" + fecha_peru + "/TIFF/GEOGRAPHIC//WGS84/decrease_floods/region" + classify + "peru_decrease_" + fecha_peru + ".tif"
print(peru)
print(" ")
print(" ")


latin2 = arcpy.Raster(latin)

# Variables de entorno
arcpy.env.snapRaster = latin2
arcpy.env.extent = latin2
arcpy.env.cellSize = latin2
arcpy.env.mask = latin2


# Union de archivos con Raster calculator
print("Uniendo El Salvador a latin...")
resultado0 = Con(IsNull(elsalvador), latin, elsalvador)
resultado0.save(latin_elsalvador)

print("Uniendo Ahuachapan a latin...")
resultado1 = Con(IsNull(ahuachapan), resultado0, ahuachapan)
resultado1.save(latin_elsalvador_ahuachapan)

print("Uniendo Valle a latin...")
resultado2 = Con(IsNull(valle), resultado1, valle)
resultado2.save(latin_elsalvador_ahuachapan_valle)

print("Uniendo Honduras a latin...")
resultado3 = Con(IsNull(honduras), resultado2, honduras)
resultado3.save(latin_elsalvador_ahuachapan_valle_honduras)

print("Uniendo Peru a latin...")
resultado4 = Con(IsNull(peru), resultado3, peru)
print(" ")
print(" ")

print("Guardando archivo final...")
resultado4.save(output_latin)
print(" ")
print(" ")

raster_tiff = output_latin
print("convirtiendo a ascii...")
ascii_final = r"T://GISDATA_terra//outputs//Latin//" + fecha_lat + "//ASCII//decrease//region" + classify + "latin_decrease_" + fecha_lat + ".asc"
ascii_converter = arcpy.RasterToASCII_conversion(raster_tiff, ascii_final)


print("Proceso terminado")
