# Sonar Exporter

[![Python](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)](https://python.org)

## Introducción

Sonar Exporter es un proyecto desarrollado con Python y PyCharm, con el objetivo de poder descargar datos de **Sonarqube**, como por ejemplo los datos de usuarios, grupos, proyectos y métricas de proyectos.

Estos datos pueden posteriormente importarse en una base de datos para su análisis, pudiendo utilizarse para diferentes propósitos, como el inventariado o el análisis de la calidad.

Este repo se ha creado para complementar el Post [Python – Exportando datos de Sonar con sonar-exporter](https://elwillie.es/2023/04/03/python-exportando-datos-de-sonar-con-sonar-exporter/) del Blog [El Willie - The Geeks invaders](https://elwillie.es)

Para la ejecución sobre MiniKube te puede interesar leer los Posts [Introducción a MiniKube e instalación en Windows 11](https://elwillie.es/2022/11/15/kubernetes-introduccion-a-minikube-e-instalacion-en-windows-11/) y [Administración fácil y rápida con K9s](https://elwillie.es/2022/11/15/kubernetes-administracion-facil-y-rapida-con-k9s/).

Si necesitas una introducción a SonarQube, te puede interesar leer el Post [SonarQube – Introducción e instalación de SonarQube, SonarScanner CLI, y SonarLint](https://elwillie.es/2022/12/11/sonarqube-introduccion-e-instalacion-de-sonarqube-sonarscanner-cli-y-sonarlint/)

**Puedes apoyar mi trabajo haciendo "☆ Star" en el repo o nominarme a "GitHub Star"**. Muchas gracias :-) 

[![GitHub Star](https://img.shields.io/badge/GitHub-Nominar_a_star-yellow?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://stars.github.com/nominate/)


## Arquitectura de la Solución

Se trata de un programa de línea de comandos en Python, que accede a la API de SonarQube, para descargar los datos que necesita, generando ficheros CSV en la carpeta ./export/ para que puedan ser utilizados para un posterior análisis y tratamiento.

### Información que se desea obtener

* Usuarios, Grupos, y pertenencia de Usuarios a Grupos de Sonar
* Proyectos de Sonar
* Un conjunto de métricas o medidas predefinida (ej: ncloc, comment_lines, coverage, bugs, code_smells, etc) de los Proyectos

Estos datos se obtienen a través de llamadas a la API de Sonar, para su procesamiento y exportación a ficheros CSV.


### Ejemplos de configuración y ejecución

Es un programa de línea de comandos, que espera recibir dos parámetros:

* **Acción que se desea realizar**. Básicamente es indicar qué datos deseamos exportar, que se generarán en la **carpeta ./export/**. Si queremos exportar varios datos (ej: usuarios de Sonar y Grupos de Sonar) bastará con ejecutarlo dos veces, en cada una especificando una acción.
* **Fichero de configuración**. Proporciona los datos de conexión en un fichero json con una formato determinado ubicado en la **carpeta ./config/** (datos de conexión a SonarQube).

El fichero JSON de configuración para la conexión con Sonar (ej: **./config/sonar_conn_elwillie.json**) será similar al siguiente, en el que especificaremos un nombre para el servidor Sonar, protocolo, nombre DNS ó dirección IP, y un Token. Es recomendable utilizar las credenciales de un usuario con **permisos de Admin**, para garantizar que tiene permisos a todos los endpoint de la API de Sonar. 
```
{
  "sonar-site": "elwillie",
  "sonar-protocol": "http",
  "sonar-domain-name": "sonar.willie.lan",
  "sonar-token": "squ_0800c3b9f720aa1de9284025bbda13adb49920b7"
}
```

**Las carpetas ./config/ y ./export/ están añadidas al fichero .gitignore**, para evitar que se puedan subir tanto credenciales como datos a los repos remotos de Git, tanto por privacidad, como por intentar mantener el repo limpio (evitar subir exportaciones de diferentes pruebas, que no aportan valor en el repo remoto). Sin embargo, si se incluiran al construir nuestra imagen Docker en local, lo que nos permitirá utilizar nuestras configuraciones tanto para ejecutar en local con Python como en local con Docker, Docker Compose, o Kubernetes.

Si tenemos varios servidores de Sonar, podemos crear múltiples ficheros de configuración (los que necesitemos) y ejecutar varias veces el programa.

A continuación se muestra un ejemplo de uso.

```
python sonar-exporter.py -c sonar_conn_elwillie.json -a export_all_sonar_users
python sonar-exporter.py -c sonar_conn_elwillie.json -a export_all_sonar_groups_and_members
python sonar-exporter.py -c sonar_conn_elwillie.json -a export_all_sonar_projects_with_metrics
```


## Otros detalles de interés

Si te interesa aprender Python, tienes disponibles los siguientes [cursos gratuitos de Python en Edube - OpenEDG](https://edube.org/):

* Python Essentials 1
* Python Essentials 2
* Python Advanced 1 – OOP
* Python Advanced 2 – Best Practices and Standardization
* Python Advanced 3 – GUI Programming
* Python Advanced 4 – RESTful APIs
* Python Advanced 5 – File Processing

Otro recurso muy interesante es [Real Python](https://realpython.com/), donde podrás encontrar tutoriales, baterías de preguntas para ponerte a prueba (quizzes), etc.

En mi Blog personal ([El Willie - The Geeks invaders](https://elwillie.es)) y en mi perfil de GitHub, encontrarás más información sobre mi, y sobre los contenidos de tecnología que comparto con la comunidad.

[![Web](https://img.shields.io/badge/GitHub-ElWillieES-14a1f0?style=for-the-badge&logo=github&logoColor=white&labelColor=101010)](https://github.com/ElWillieES)

# Git

## Repositorio

Este repo se puede clonar desde GitHub utilizando este [enlace HTTP](https://github.com/ElWillieES/sonar-exporter.git). 

A continuación se muestra el comando git clone usando SSH en lugar de HTTP.

```sh
git clone git@github.com:ElWillieES/sonar-exporter.git
```

## Estructura de Ramas: Trunk Based Development (TBD)

* **Ramas permanentes**. Utilizaremos **master** como rama principal.
* **Ramas temporales o efímeras**. Utilizaremos **feature/xxx** (nueva característica) y/o **hotfix/xxx** (corregir un bug crítico urgente), que nacen de la rama principal y mezclan de nuevo sobre ella mediante Merge Request.
* **Gestión de Releases**. Para cada Release generaremos una etiqueta (tag) del tipo **release/a.b.c**.

En la descripción de las ramas de feature y hotfix, se especificará el ID de la tarea o issue asociada, por ejemplo:

```git
feature/3813
hotfix/2262
```

Si necesitáramos varias ramas para una misma tarea, añadiremos un número secuencial para evitar la colisión:

```git
feature/3813-1
feature/3813-2
```

## Commits Semanticos: icónos y prefijos

Como recomendación y buena práctica, el título para los Commits y de las Merge Request, pueden empezar con un icono y un prefijo, seguido de dos puntos y de un mensaje corto que comience por un verbo imperativo (ej: add, change, fix, remove, etc.). Por ejemplo:

```git
✨ feat(backend): add support for users having multiple suscriptions
```

Prefijos:

```git
feat: Nueva característica
fix: Corrección a un error
doc: Documentación
style: Cambios de formato (guía de estilo)
refactor: Renombrar una variable, simplificar un método, etc…
test: Añadir o modificar tests
chore: Rareas rutinarias, como modificar el .gitignore, etc…
```

Iconos:

```git
💄 Cosmetic
🎨 Improve format / structure
🛠/🐛 Fix
✨ Feature
🚑 Hotfix
📝 Doc
🚀 Release
♻ Refactor
🐳 Devops
☸ Kubernetes
🧪 Arquitectura de tests
✅ Añadir un Test
✔ Hacer que un test pase
💩 Ñapas
🏗 Architectural changes
🤡 Mocks
💚 Fixing Build
📈 Analiltycs
🌐 Localizations
😒 Chore
💫 Animations & Transitions
♿ Accesibility
🚧 Feature work in progress
🚀 Launch a new build
```

# Docker - Ejecución en local

## Con Docker

Se puede ejecutar la aplicación en local con Docker. 

Los siguientes comandos ejecutados en la raíz del Proyecto, muestran:
* Cómo **crear una imagen** en local con docker build. Antes de construir la imagen, borramos el contenido de app/export/, por si tuviéramos ficheros de pruebas de ejecución, para no engordar y ensuciar la imagen.
* Cómo listar las imágenes que tenemos disponibles en local. Deberá aparecer la que acabamos de crear.
* **Cómo ejecutar un contenedor con nuestra imagen, con el comando deseado**. Como nuestra aplicación es de línea de comandos, se incluyen varios ejemplos, en cada uno de los cuales se indica como parámetro el fichero de configuración que necesita (debe existir en la carpeta /usr/src/app/config/ del contenedor) y la acción a realizar (hay varias posible, según los datos que queramos exportar). Como se van a generar los ficheros de exportación en la carpeta del contenedor /usr/src/app/export, y los contenedores son efímeros, **utilizamos un volumen sobre /usr/src/app/export para que los datos persistan** y además podamos acceder a los ficheros que hemos generado. Es necesario especificar la ruta absoluta del host (ajustarla con la de cada uno).  

```shell
rm app/export/*

docker build -t sonar-exporter .
docker images

docker run -v d:/code/elwillie/sonar-exporter/app/export:/usr/src/app/export --rm sonar-exporter python sonar-exporter.py -c sonar_conn_elwillie.json -a export_all_sonar_users
docker run -v d:/code/elwillie/sonar-exporter/app/export:/usr/src/app/export --rm sonar-exporter python sonar-exporter.py -c sonar_conn_elwillie.json -a export_all_sonar_groups_and_members
docker run -v d:/code/elwillie/sonar-exporter/app/export:/usr/src/app/export --rm sonar-exporter python sonar-exporter.py -c sonar_conn_elwillie.json -a export_all_sonar_projects_with_metrics
```

Podemos arrancar una sesión interativa de Bash sobre un Contendor con nuestra imagen Docker, para de este modo, analizar mejor incidencias y problemas que nos puedan surgir, depurar, etc. Suele ser bastante útil.

En el siguiente ejemplo, arrancamos una sesión bash sobre un contenedor con nuestra imagen y un volumen mapeando la carpeta export de nuestro portátil con la del contenedor, ejecutamos sonar-exporter para exportar los usuarios de Sonar, y salimos del contenedor.

```shell
docker run --rm -v d:/code/elwillie/sonar-exporter/app/export:/usr/src/app/export -it sonar-exporter /bin/bash
python sonar-exporter.py -c sonar_conn_elwillie.json -a export_all_sonar_users
exit
```


## Con Docker Compose

El siguiente comando ejecutado en la raíz del Proyecto, muestra cómo compilar (es decir, construir la imagen Docker) y ejecutar sonar-exporter con Docker Compose, así como la forma de poder comprobar los logs de su ejecución.

Si observamos el fichero **docker-compose.yml**, podemos ver que incluye varias ejecuciones de sonar-exporter, para las diferentes exportaciones que queremos realizar. Además, utiliza un volumen mapeando la carpeta export de nuestro portátil con la del contenedor, para así poder acceder a los datos generados desde nuestro portátil, después de su ejecución. 

```shell
docker-compose -f docker-compose.yml up --build -d
docker-compose -f docker-compose.yml logs
```


# Kubernetes - Ejecución en local (MiniKube)

Se puede ejecutar la aplicación en local con Kubernetes, si tienes instalado MiniKube. Para ampliar información te puede interesar leer [Introducción a MiniKube e instalación en Windows 11](https://elwillie.es/2022/11/15/kubernetes-introduccion-a-minikube-e-instalacion-en-windows-11/)

Los manifiestos de Kubernetes, están en la carpeta kube, y son los siguientes:

* **exporter-ns.yml**. Para la creación del namespace exporter, donde desplegaremos nuestra aplicación.
* **sonar-exporter-conf.vol**. Permite crear un Volumen, es decir, un PersistentVolume de tipo hostPath y un PersistentVolumeClaim, que mapearemos a nuestro Job para tener persistencia entre ejecuciones. Los datos persistirán dentro del almacenamiento de MiniKube (nos podemos conectar con minikube ssh para verlos). 
* **sonar-exporter-conf.yml**. Permite crear un ConfigMap, que contiene el fichero JSON de configuración que necesitamos para conectarnos a la API de Sonar. Los mapearemos a los contenedores sobre el directorio /usr/src/app/config sobrescribiendo los ficheros que pudiera haber en la imagen original.
* **sonar-exporter-job.yml**. Consiste en un Job que incluye un contenedor para cada comando que queremos ejecutar (en nuestro caso de ejemplo son tres), y mapea tanto el ConfigMap anterior como el volumen persistente.

Los siguientes comandos ejecutados en la raíz del Proyecto, muestran cómo tagear la Imagen Docker para subirla al Registry local de MiniKube.

```shell
docker tag sonar-exporter localhost:5000/sonar-exporter
docker push localhost:5000/sonar-exporter
```

Realizado esto, en la ventana Terminal de PyCharm, podemos ejecutar los siguientes comandos para aplicar los manifiestos en nuestro Cluster de MiniKube (namespace y Job), y consultar el Log de ejecución del Job que acabamos de crear y ejecutar (la salida del Log, será igual a cuando lo ejecutamos en Docker o directamente en PyCharm).

```shell
cd kube
kubectl apply -f exporter-ns.yml
kubectl apply -f sonar-exporter-vol.yml
kubectl get PersistentVolume -n exporter -o wide
kubectl get PersistentVolumeClaim -n exporter -o wide

kubectl apply -f sonar-exporter-conf.yml
kubectl apply -f sonar-exporter-job.yml

kubectl get jobs -n exporter
kubectl describe jobs sonar-exporter -n exporter

kubectl logs job/sonar-exporter -c sonar-exporter-sonar-users -n exporter
kubectl logs job/sonar-exporter -c sonar-exporter-sonar-groups -n exporter
kubectl logs job/sonar-exporter -c sonar-exporter-sonar-projects -n exporter
```

Si queremos ver o incluso editar el ConfigMap, podemos utilizar el siguiente comando.

```shell
kubectl edit configmap sonar-exporter-conf -n exporter
```

También podemos crear un nuevo contenedor al vuelo, con nuestra imagen, con una sesión bash a la que conectarnos para poder depurar y hacer pruebas.

```shell
kubectl run -it --rm sonar-exporter --image=localhost:5000/sonar-exporter -n exporter -- /bin/bash
```

Si necesitamos volver a crear el Job, tendremos que eliminarlo antes, para lo cual podemos utilizar un comando como el siguiente.

```shell
kubectl delete job sonar-exporter -n exporter
```

Al finalizar podemos eliminar el namespace de Kubernetes, para eliminar todos los recursos y dejar "la casa limpia".

```shell
kubectl delete ns exporter
```


# Contactos

| Nombre        | Posición en el Proyecto | Email                                                |
|---------------|-------------------------|------------------------------------------------------|
| **El Willie** | Brownie Manager         | [elwillieES@gmail.com](mailto:elwillieES@gmail.com)  |
