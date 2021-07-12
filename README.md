# Objetivo

El objetivo de este proyecto es aprender a modelar un problema en CNF, y a usar un SAT solver para resolverlo, así como traducir la salida del SAT solver a un formato legible.
No solo se evaluará que la implementación funcione, sino la eficiencia de su traducción a CNF del problema.

# Problema a resolver

Imagine que se está organizando un torneo, y se le pide realizar un programa que encuentre una asignación de fecha y hora en la que los juegos van a ocurrir. Las reglas son las siguientes:

* Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales". Esto significa que, si hay 10 equipos, cada equipo jugará 18 veces.
* Dos juegos no pueden ocurrir al mismo tiempo.
* Un participante puede jugar a lo sumo una vez por día.
* Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos.
* Todos los juegos deben empezar en horas "en punto" (por ejemplo, las 13:00:00 es una hora válida pero las 13:30:00 no).
* Todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas. Pueden ocurrir juegos en dichas fechas.
* Todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo.
* A efectos prácticos, todos los juegos tienen una duración de dos horas.

# Formato de entrada

Su sistema debe recibir un JSON con el siguiente formato (asuma que siempre recibirá el formato correcto):

```
{
  "tournament_name": String. Nombre del torneo,
  "start_date": String. Fecha de inicio del torneo en formato ISO 8601,
  "end_date": String. Fecha de fin del torneo en formato ISO 8601,
  "start_time": String. Hora a partir de la cuál pueden ocurrir los juegos en cada día, en formato ISO 8601,
  "end_time": String. Hora hasta la cuál pueden ocurrir los juegos en cada día, en formato ISO 8601,
  "participants": [String]. Lista con los nombres de los participantes en el torneo
}
```

Asuma que todas las horas vienen sin zona horaria especificada, y asuma por lo tanto que su zona horaria es UTC.

# Actividad 1

Deben crear una traducción del problema a formato CNF, y luego deben crear un programa, en el lenguaje de programación que sea de su agrado, que traduzca cualquier JSON en el formato propuesto a la representación del problema en formato [DIMACS CNF](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html)

# Actividad 2

Usando la transformación creada en la parte anterior, los archvios en formato DIMACS CNF pueden ser usados como entrada para el SAT solver [Glucose](https://www.labri.fr/perso/lsimon/glucose/). Debe crear un programa, en el lenguaje de programación que sea de su agrado, que traduzca la salida de Glucose al resolver el problema en un archivo con el mismo nombre del torneo y extensión `.ics`, en formato de [iCalendar](https://en.wikipedia.org/wiki/ICalendar) de manera que sea posible agregar la asignación de los juegos a un gestor de calendarios. Para ello puede usar cualquier librería que considere necesaria. Los eventos del calendario deben tener ocurrir a la hora que fue asignada cumpliendo todas las reglas dadas, y deben indicar quiénes son los participantes en el juego, quién es el "local" y quién es el "visitante".

# Actividad 3

Debe crear un cliente que maneje todo el proceso. Es decir, reciba un JSON en el formato de entrada, ejecute el programa que lo transforma en CNF, introduzca el resultado  en Glucose, y se asegure de que se cree el archivo .ics con la respuesta, o falle en caso de ser UNSAT. Debe generar casos de prueba fáciles y difíciles, y medir el rendimiento de su solución.

# Entrega

Deben tener un repositorio con todo el código usado y un informe que describa su solución, sus resultados experimentales, así como instrucciones específicas para ejecutar todo el proceso.
