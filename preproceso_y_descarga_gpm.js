// *************************************************************************************************** //
// *************************************************************************************************** //
//        PRE-PROCESO DE INFORMACIÓN DE PRECIPITACIÓN DE GPM PARA ACTUALIZACIÓN DE TERRA-I             //
//                                                                                                     //
//                         Elaborado por Jorge Andres Perez 09-12-2019                                 //
// *************************************************************************************************** //
// *************************************************************************************************** //

// =================================================================================================== //
//                                     DATOS DE ENTRADA                                                //
// =================================================================================================== //
var TRMM3B42 = ee.ImageCollection("TRMM/3B42")
var GPMV06 = ee.ImageCollection("NASA/GPM_L3/IMERG_V06")
var zoi = ee.FeatureCollection("users/jorgeperez/terra-i_trmm_mask")

// =================================================================================================== //
//                             CAMBIO EN FECHAS DE PROCESAMIENTO                                       //
// =================================================================================================== //

// --------------------------------------------------------------------------------------------------- //
// En el siguiente paso, se debe cambiar la fecha y la de inicio y la fecha final                      //
// startDateStringYear = año inicial                                                                   //
// startDateStringMonth = mes inicial                                                                  //
// startDateStringDay = día inicial                                                                    //
// endDateStringYear = año final                                                                       //
// endDateStringMonth = mes final                                                                      //
// endDateStringDay = día final                                                                        //
//                                                                                                     //
// Ejemplo. si se va a descargar los datos para el 5 marzo del 2020, se deben tomar las siguientes     //
//  - Fecha inicio: 2020-01-01                                                                         //
//  - Fecha final: 2020-03-20                                                                          //
//     - NOTA: como se va a procesar la fecha 5 de marzo, se deben tomar los datos que abarque los     //
//             los 16 días que le coresponden. Es decir, 5 de marzo mas 16 días                        //
// --------------------------------------------------------------------------------------------------- //

var startDateStringYear = '2022'; // CAMBIAR EL AÑO DE INICIO SI ES NECESARIO
var startDateStringMonth = '01';
var startDateStringDay = '01';
var startDateString = startDateStringYear+'-'+startDateStringMonth+'-'+startDateStringDay;

var endDateStringYear = '2022'; // PONER EL MISMO AÑO DE LA LÍNEA 25
var endDateStringMonth = '08'; // CAMBIAR AL MÉS DE PROCESAMIENTO
var endDateStringDay = '01'; // CAMBIAR AL DÍA DE PROCESAMIENTO
var endDateString = endDateStringYear+'-'+endDateStringMonth+'-'+endDateStringDay;                        

var startDateStringYearNumber = ee.Number.parse(startDateStringYear);
var endDateStringYearNumber = ee.Number.parse(endDateStringYear);

var startDate = ee.Date(startDateString);
var endDate = ee.Date(endDateString);

print('Fecha de inicio',startDateString);
print('Fecha final',endDateString);

// =================================================================================================== //
// =================================================================================================== //
//                                          FUNCTIONS
// =================================================================================================== //
// =================================================================================================== //

// --------------------------------------------------------------------------------------------------- //
// - Función gte0 = Elimina los valores negativos en los datos GPM                                     //
// - Función Resampled = Cambia la resolución espacial de GPM al tamaño de TRMM                        //
// - Función normalize_resample = Normaliza los datos GPM                                              //
// --------------------------------------------------------------------------------------------------- //
function gte0(image){
  var maskGPM = image.gte(0);
  var precipitationGPM = image.updateMask(maskGPM);
  return precipitationGPM;
}

function Resampled(image){
  var resampled = image.resample().reproject({
    crs: 'EPSG:4326',
    scale: 27880.67412
  });
  return resampled;
}

function normalize_resample(image){
  var max = image.reduceRegion({
    reducer: ee.Reducer.max(),
    geometry: zoi,
    scale: 27880.67412,
    maxPixels: 10000000000
    }
  );

  var max1 = max.values();
  max1 = ee.Number(max1.get(0));
  
  var imagen_normalizada = image.expression(
    'image/max',{
      'image':image,
      'max':max1
    }
  );
  return imagen_normalizada;
} 

// =================================================================================================== //
// =================================================================================================== //
//                                        TEMPORALIDAD
// =================================================================================================== //
// =================================================================================================== //

// --------------------------------------------------------------------------------------------------- //
// nDay = cantidad de imágenes (cada 16 días) que se encuentran en un año.                             //
// --------------------------------------------------------------------------------------------------- //
var nDay = ee.Number(endDate.difference(startDate,'day')).round();
var nDay16 = nDay.divide(ee.Number(16)).round();
print('Cantidad de días:',nDay);
print('Cantidad de imágenes disponibles cada 16 días:',nDay16);

// =================================================================================================== //
// =================================================================================================== //
//                                      FILTRADO DE COLECCIÓN
// =================================================================================================== //
// =================================================================================================== //

// --------------------------------------------------------------------------------------------------- //
// f1_GPMV06 = colección de imágenes filtradas de GPM versión 6                                        //
// --------------------------------------------------------------------------------------------------- //
var f1_GPMV06 = GPMV06
  .filterDate(startDate,endDate)
  .filterBounds(zoi)
  .select('precipitationCal')
  .map(gte0);

// =================================================================================================== //
// =================================================================================================== //
//                                  COLLECCIÓN CADA 16 DÍAS                                            //
// =================================================================================================== //
// =================================================================================================== //
// --------------------------------------------------------------------------------------------------- //
// creación de imágenes cada 16 días de GPM v06                                                        //
// --------------------------------------------------------------------------------------------------- //
var by16DayGPMV06 = ee.ImageCollection(
  ee.List.sequence({
    start: 0,
    end: nDay,
    step: 16
    }
  ).map(function(n){
    var ini = startDate.advance(n,'day');
    var end = ini.advance(16,'day');
    
    // filter and reduce
    var f1GPMV06 = f1_GPMV06.filterDate(ini,end)
                    .sum()
                    .set('system:time_start', ini);
                    
    return f1GPMV06;
  })
);
var by16DayGPMV06resampled = by16DayGPMV06.map(Resampled).map(normalize_resample);
print('Colección de imágenes GPM cada 16 días',by16DayGPMV06resampled);

// =================================================================================================== //
// =================================================================================================== //
//                                          MAPEAR IMÁGENES                                            //
// =================================================================================================== //
// =================================================================================================== //
// --------------------------------------------------------------------------------------------------- //
// Visualización de la última imágen en el pantrópico                                                  //
// --------------------------------------------------------------------------------------------------- //
Map.centerObject(zoi);
Map.addLayer(zoi,{},"zoi");
Map.addLayer(by16DayGPMV06resampled.reduce(ee.Reducer.last()).clip(zoi),{},"Visualización de la última imagen GPM en el pantrópico");

// =================================================================================================== //
// =================================================================================================== //
//                               EXPORTAR COLECCIÓN DE IMÁGENES                                        //
// =================================================================================================== //
// =================================================================================================== //
// --------------------------------------------------------------------------------------------------- //
// exportCollection = función para exportar la colección de imágenes                                   //
// --------------------------------------------------------------------------------------------------- //
function exportCollection(collection,n){
  
  var collectionList = collection.toList(n);
  var nCollectionList = collectionList.size().getInfo();
  
  for(var i = 0; i < nCollectionList; i++){
    var img = ee.Image(collectionList.get(i));
    
    var id = img.id().getInfo();
    //print('id', id)
    var idNumber = ee.Number.parse(id).multiply(16).add(1)
    //print("idNumber",idNumber)
    var idString = (idNumber.getInfo())
    print('idString', idString)
    var region = zoi;
    
    Export.image.toDrive({
      image:img.clip(zoi).float(),
      description: 'gpm_' + startDateStringYear + '_' + idString,
      folder: 'GPM',
      fileNamePrefix: 'gpm_' + startDateStringYear + '_' + idString,
      region: region,
      scale: 27880.67412,
      maxPixels: 10000000000
    });
  }
}

var exportar = exportCollection(by16DayGPMV06resampled,nDay16);
