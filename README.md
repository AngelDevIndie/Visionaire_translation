# Visionaire_translation

Scripts para exportar e importar texto de los archivos vbin de Visionaire.

PASOS:
- Extraer el vbin con vis5ext o unpakke.
- Usar el script Visionaire_export con el vbin
- Traducir el texto con Notepad++ marcando la opción "Codificar en UTF-8 sin BOM"
- Usar el script Visionaire_imort con el vbin
- Empaquetar con unpakke todos los recursos.
- El archivo resultante debe llamarse igual que el original *.vis

UPDATE 2/23
- Se puede convetir un vbin, o veb que es lo mismo, con el motor oficial a formato ved, que es un XML.
- O se puede extraer los textos en formato .po y luego importarlos para luego grabarlo en formato veb o vbin.
- Usar unpakke para comprimir todos los recursos.
|-> NOTA: unpakke cuando comprime tiene en cuenta el orden alfabetico de los nombres de los archivos para comprimir. Y esto es importante para la numeración de los recursos.
- TENGO MÁS INFORMACIÓN POR INTRODUCIR EN ESTE ARCHIVO.
