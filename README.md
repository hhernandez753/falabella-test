# Prueba Técnica
REST API con los siguientes Endpoint:
+ /patent-domain/<domain>
  Metodo: GET
  Parametro URL: domain obligatoiro. Ej.: AAAA000
  Respuesta: Objeto JSON. Forma: {"mssg": "<Mensaje>", "patentId": <ID de Patente (Int)>}
  Ejemplo Petición: http://<Host>/patent-domain/AAAA000

+ /patent-id/<id>
  Metodo: GET
  Parametro URL: id obligatoiro. Ej.: 1000
  Respuesta: Objeto JSON. Forma: {"mssg": "<Mensaje>", "patentDomain": <Código Alfanumérico de Patente (String)>}
  Ejemplo Petición: http://<Host>/patent-id/1000
  
+ /matrix-sum
  Metodo: POST
  Header: Content-Type:  application/json
  Body: Objeto JSON. Forma: {"R": <Int > 0>, "C": <Int > 0>, "Z": <0 < Int <= 1.000.000>, "X": <Int >= 0>, "Y": <Int >= 0>}
  Respuesta: Objeto JSON. Forma: {"mssg": "<Mensaje>", "sum": <Sumatoria de la Matriz (Int)>}
  Ejemplo Petición: http://<Host>/matrix-sum

# Dependecias
+ pyhton3 (>=3.5)
+ pip3 install Flask
+ pip3 install numpy

# Ejecutar y probar aplicación
+ python3 web_server.py
+ URL Base de la API: http://localhost:8080
