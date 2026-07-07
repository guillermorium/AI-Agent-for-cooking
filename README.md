
## OBJETIVO

Un agente de IA que aporte ideas de recetas sobre un plan semanal variado de comidas y cenas. Con él, evitarás
la búsqueda por internet de la receta y no tendrás la obligación de dar tus datos en todas las páginas que abras
sobre la receta en cuestión. Además, te ayudará con el cálculo de los macros.

La salida del agente estará estructurada en partes:
- Introducción
- Ingredientes
- Elaboración
- Consejos o variaciones
- Macronutrientes

## IDEAS
- Da ideas de recetas según la estación del año (para recomendar aquellos platos que sientan mejor con el frío
o con el calor)
- Busca la receta en una bibliografía de documentos guardados en local (libros de recetas, recetarios o
libros de cocina)
- Ideas de recetas según los ingredientes que tengas en el frigorífico o quieras gastar porque
se están poniendo malos.
- Calcula los macros de la receta que te está dando, y puede coordinarlos con la receta de la cena
para cubrir algún objetivo de ganancia muscular.
- El agente tendrá dos tipos de memoria: largo plazo (con las recetas hechas hasta el momento), a la que se añadirá la
receta final elegida en la conversación; y corto plazo (los mensajes de la conversación mantenida), que servirá al 
método recipe_output() para redactar la receta y exportarla (tras eso, se borrará).

## ISSUES
- Gestionar la memoria a largo plazo con el fichero json.
- Pensar como inyectar el nombre de la receta final en el método recipe_response(), al menos la propuesta de receta.
- Manejar la confirmación de receta con 'ok' y 'no' y los mensajes del agente. Afinar su system prompt.


YO: Que puedo comer hoy?
AGENTE: 
      Receta      | Dificultad | Tiempo estimado
Ensalada de arroz | 2/10 | 30 min
Cocido            | 8/10 | 2 h
YO: Cocido
AGENTE:
Te cuento la receta del cocido y la exporto como pdf.