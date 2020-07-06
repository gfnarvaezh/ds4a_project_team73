def get_ordered_variables():
    return {
        'FAMI_ESTRATOVIVIENDA':['No data', 'Sin Estrato', 'Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5', 'Estrato 6'],
        'FAMI_PERSONASHOGAR':['No data', '1 a 2', '3 a 4', '5 a 6', '7 a 8', '9 o más'],
        'FAMI_CUARTOSHOGAR': ['No data','Uno', 'Dos', 'Tres', 'Cuatro', 'Cinco', 'Seis o mas'],
        'FAMI_EDUCACIONPADRE': ['No data', 'No Aplica', 'No sabe', 'Ninguno', 'Primaria incompleta', 'Primaria completa', 'Secundaria (Bachillerato) incompleta', 'Secundaria (Bachillerato) completa', 'Técnica o tecnológica incompleta', 'Técnica o tecnológica completa', 'Educación profesional incompleta', 'Educación profesional completa', 'Postgrado'],
        'FAMI_EDUCACIONMADRE': ['No data', 'No Aplica', 'No sabe', 'Ninguno', 'Primaria incompleta', 'Primaria completa', 'Secundaria (Bachillerato) incompleta', 'Secundaria (Bachillerato) completa', 'Técnica o tecnológica incompleta', 'Técnica o tecnológica completa', 'Educación profesional incompleta', 'Educación profesional completa', 'Postgrado'],
        'FAMI_NUMLIBROS': ['No data', '0 A 10 LIBROS', '11 A 25 LIBROS', '26 A 100 LIBROS', 'MÁS DE 100 LIBROS'],
        'FAMI_COMELECHEDERIVADOS': ['No data', 'Nunca o rara vez comemos eso', '1 o 2 veces por semana', '3 a 5 veces por semana', 'Todos o casi todos los días'],
        'FAMI_COMECARNEPESCADOHUEVO': ['No data', 'Nunca o rara vez comemos eso', '1 o 2 veces por semana', '3 a 5 veces por semana', 'Todos o casi todos los días'],
        'FAMI_COMECEREALFRUTOSLEGUMBRE': ['No data', 'Nunca o rara vez comemos eso', '1 o 2 veces por semana', '3 a 5 veces por semana', 'Todos o casi todos los días'],
        'FAMI_SITUACIONECONOMICA': ['No data', 'Peor', 'Igual', 'Mejor'],
        'ESTU_DEDICACIONLECTURADIARIA': ['No data', 'No leo por entretenimiento', '30 minutos o menos', 'Entre 30 y 60 minutos', 'Entre 1 y 2 horas', 'Más de 2 horas'],
        'ESTU_DEDICACIONINTERNET': ['No data', 'No Navega Internet', '30 minutos o menos', 'Entre 30 y 60 minutos', 'Entre 1 y 3 horas', 'Más de 3 horas'],
        'ESTU_HORASSEMANATRABAJA': ['No data', '0', 'Menos de 10 horas', 'Entre 11 y 20 horas', 'Entre 21 y 30 horas', 'Más de 30 horas']        
    }

def get_numerical_variables():
    return ['PUNT_LECTURA_CRITICA',
            'PERCENTIL_LECTURA_CRITICA',
            'DESEMP_LECTURA_CRITICA',
            'PUNT_MATEMATICAS',
            'PERCENTIL_MATEMATICAS',
            'DESEMP_MATEMATICAS',
            'PUNT_C_NATURALES',
            'PERCENTIL_C_NATURALES',
            'DESEMP_C_NATURALES',
            'PUNT_SOCIALES_CIUDADANAS',
            'PERCENTIL_SOCIALES_CIUDADANAS',
            'DESEMP_SOCIALES_CIUDADANAS',
            'PUNT_INGLES',
            'PERCENTIL_INGLES',
            #'DESEMP_INGLES',
            'PUNT_GLOBAL',
            'PERCENTIL_GLOBAL',
            'ESTU_INSE_INDIVIDUAL',
            'ESTU_NSE_ESTABLECIMIENTO',
            'ESTU_NSE_INDIVIDUAL']

def get_irrelevant_variables():
    return [
    'ESTU_TIPODOCUMENTO', #Ya tenemos edad y nacionalidad
    'PERIODO', #tienen el mismo valor en todo el archivo
    'ESTU_ESTUDIANTE', # Solo tiene un valor
    'ESTU_CONSECUTIVO', #no ofrece información, es un codigo unico del estudiante
    'ESTU_COD_RESIDE_DEPTO', #Es un codigo, pero ya tenemos el nombre del dpto
    'ESTU_COD_RESIDE_MCPIO', #Mismo de arriba
    'COLE_CODIGO_ICFES', #Ya tenemos el nombre del colegio
    'COLE_COD_DANE_ESTABLECIMIENTO', #Misma de arriba
    'COLE_COD_DANE_SEDE', #No da info adicional, salvo si el colegio tiene diferentes sedes
    'COLE_NOMBRE_SEDE', #Mismo de arriba
    'COLE_COD_MCPIO_UBICACION', #Solo daría información en caso de que el estudiante se tenga que desplazar desde su municipio a otro para ir al colegio
    'COLE_MCPIO_UBICACION', #Mismo de arriba
    'COLE_COD_DEPTO_UBICACION', #Mismo de arriba
    'COLE_DEPTO_UBICACION', #Mismo de arriba
    'ESTU_COD_MCPIO_PRESENTACION', #Solo daría información en caso de que el estudiante se tenga que desplazar desde su municipio a otro para presentar el examen
    'ESTU_MCPIO_PRESENTACION', #Mismo de arriba
    'ESTU_DEPTO_PRESENTACION', #Mismo de arriba
    'ESTU_COD_DEPTO_PRESENTACION', #Mismo de arriba
    'ESTU_ESTADOINVESTIGACION', #Es una columna con información administrativa sobre el resultado del examen
    'ESTU_GENERACION-E', #Es un subsidio basado en el resultado del examen, no nos interesa
    'COLE_SEDE_PRINCIPAL', #No aporta información
    'ESTU_PRIVADO_LIBERTAD', #muy pocos casos
    ]

def get_unused_variables():
    return [
    'COLE_NOMBRE_ESTABLECIMIENTO',
    'ESTU_ETNIA',
    'ESTU_MCPIO_RESIDE',
    'ESTU_PAIS_RESIDE',
    'DESEMP_INGLES',
    'ESTU_TIPOREMUNERACION',
    'DESEMP_INGLES'
    ]

def get_order_variables_model():
    return [
    'EDAD',
    'FAMI_ESTRATOVIVIENDA',
    'FAMI_PERSONASHOGAR',
    'FAMI_CUARTOSHOGAR',
    'FAMI_EDUCACIONPADRE',
    'FAMI_EDUCACIONMADRE',
    'FAMI_NUMLIBROS',
    'FAMI_COMELECHEDERIVADOS',
    'FAMI_COMECARNEPESCADOHUEVO',
    'FAMI_COMECEREALFRUTOSLEGUMBRE',
    'FAMI_SITUACIONECONOMICA',
    'ESTU_DEDICACIONLECTURADIARIA',
    'ESTU_DEDICACIONINTERNET',
    'ESTU_HORASSEMANATRABAJA',
    'ESTU_NACIONALIDAD',
    'ESTU_GENERO',
    'ESTU_TIENEETNIA',
    'ESTU_DEPTO_RESIDE',
    'FAMI_TRABAJOLABORPADRE',
    'FAMI_TRABAJOLABORMADRE',
    'FAMI_TIENEINTERNET',
    'FAMI_TIENESERVICIOTV',
    'FAMI_TIENECOMPUTADOR',
    'FAMI_TIENELAVADORA',
    'FAMI_TIENEHORNOMICROOGAS',
    'FAMI_TIENEAUTOMOVIL',
    'FAMI_TIENEMOTOCICLETA',
    'FAMI_TIENECONSOLAVIDEOJUEGOS',
    'COLE_GENERO',
    'COLE_NATURALEZA',
    'COLE_CALENDARIO',
    'COLE_BILINGUE',
    'COLE_CARACTER',
    'COLE_AREA_UBICACION',
    'COLE_JORNADA']

def get_scores():
    return [
    'PUNT_LECTURA_CRITICA',
    'PUNT_MATEMATICAS',
    'PUNT_C_NATURALES',
    'PUNT_SOCIALES_CIUDADANAS',
    'PUNT_INGLES'
    ]