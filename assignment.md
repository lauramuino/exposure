# Credential Exposures Scoring Challenge:

## Introducción:
El equipo de ciberinteligencia nos pide la implementación de un servicio de scoring de usuarios por credenciales expuestas.

## Detalle del desafio:
El servicio debe encargarse de recibir credenciales expuestas (como las que se ven en el archivo exposures.json) y generar un scoring de usuario (mientras más credenciales haya expuesto o más críticas sean esas exposiciones, más alto será su scoring).

Requerimos:
1) Cargar la información del archivo alerts.json, el cual contiene la información de las credenciales expuestas hasta la fecha.
####
2) Disponibilizar un endpoint que permita la carga de nuevas credenciales expuestas.
```
Ejemplo:

POST /exposures

body = {
          "id": "a4s81o3e-7c3b-4e0d-9b5f-2s4k7d6e4b8f",
          "email": "javier.gutierrez@gmail.com",
          "source_info": {
            "source": "data breach",
            "severity": "high"
          },
          "detected_at": "2025-09-16T18:50:13.262Z",
          "created_at": "2025-09-16T18:54:13.262Z"
        }
```
3) Asignar un scoring por usuario dependiendo de la cantidad de alertas asociadas a su mail y la criticidad de las mismas.
   1) El scoring es un número de 0 a 10.
   2) Las alertas con source malware modifican el scoring automáticamente a 10.
   3) Las alertas de tipo data breach se dividen en 2 niveles de criticidad. Las low suman 1 punto al scoring y las high suman 3.
####
4) Crear un endpoint de consulta de scoring por usuario, pasando el mail del usuario como parámetro. En caso de no pasar un valor como parámetro retornar los 3 usuarios con mayor scoring. Tener en cuenta que el equipo de seguridad va a realizar muchas más consultas a los usuarios con mayor scoring.

```
Ejemplo:

GET /scoring?email=john.wick@gmail.com

response 200:
{
  "id": a4s81o3e-7c3b-4e0d-9b5f-2s4k7d6e4b8f
  "email": john.wick@gmail.com,
  "scoring": 7
}
```

### Opcional Bonus:
Pensar un requerimiento extra que pueda serle útil al equipo de ciberinteligencia.

Además, cualquier herramienta, tecnologia o ideas que implementes, son bienvenidas. Es bienvenido cualquier esfuerzo extra incluido.
Ejemplo: usar una DB, algo que mejore tiempos de procesamiento, algo que haga sencillo la forma de correr, mas robustez, UI, extensibilidad para otras consultas, testing, etc...

## Entregable y Puntos a Evaluar
* Subir la resolución a un repo público.
* Debe de correr containerizado con Docker por lo que se requerira escribir tambien un Dockerfile.
* Escribir documentación del proyecto:
  * Explicación del proyecto
  * Instrucciones de ejecución
  * Pruebas de carga y consulta de información
  * En caso de realizar el punto bonus explicar en qué consiste y por qué decidiste ir por el camino elegido

Vamos a evaluar en base al entregable, principalmente, como solucionaste el problema, como lo pensaste y como lo implementaste. Buscamos profesionales que apunten a la autonomia y resolucion de problemas.