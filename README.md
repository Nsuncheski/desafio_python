# desafio_python


**Para ejecutar el docker compose use los siguientes comandos**:


docker compose build

docker compose up

**para utilizar las APIs que cargan la multa y piden los informes entre por el siguiente link**:

http://localhost:8000/docs

para ingresar a la interfase de streamlit ingrese aqui:

http://localhost:8501.


**Para la arquitectura de aws**:

Las apis se pueden dividir por tipo (personas, vehiculos, policias, multas),
y ser empaquetadas en lambdas AWS , para esto se deberia usar apigateway para cada una.
Para la bdd se usaria postgresql en RDS
Para los los logs quedaria con Cloudwatch
para contraseñas y nombres privados se usaria el servicio de secret Managers
SNS para enviar emails con eventos cloudwatch cuando se inserte una multa y este envie correos a las personas involucradas.
Tambien se puede agregar lambdas authorizer que sirve como autorización personalizada desde el apigateway para otorgar permisos.

# Despliegue de la aplicación

Para automatizar el proceso de despliegue de la aplicación, utilizamos AWS CodePipeline, un servicio de entrega continua que permite compilar, probar y desplegar automáticamente tu código cada vez que hay cambios en el repositorio de código fuente.

El flujo de trabajo de despliegue consta de los siguientes pasos:

1. **Recuperación del código fuente**: CodePipeline recupera el código fuente desde el repositorio de código, como GitHub o AWS CodeCommit.

2. **Compilación y pruebas**: Utilizamos AWS CodeBuild para compilar y realizar pruebas automatizadas en el código fuente. Esto garantiza que el código sea funcional y cumpla con los estándares de calidad antes de ser desplegado.

3. **Despliegue en entorno de prueba**: Una vez que las pruebas han pasado con éxito, el artefacto compilado se despliega en un entorno de prueba, que puede ser una instancia EC2 o un contenedor Docker en ECS.

4. **Pruebas en entorno de prueba**: Se realizan pruebas adicionales en el entorno de prueba para validar que la aplicación se comporte correctamente en un entorno realista.

5. **Despliegue en entorno de producción**: Después de que las pruebas en el entorno de prueba hayan sido aprobadas, el artefacto se despliega en el entorno de producción, que puede ser otra instancia EC2 o un clúster ECS.

6. **Monitoreo y gestión de cambios**: Utilizamos AWS CloudWatch para monitorear el rendimiento de la aplicación en producción y para recibir alertas en caso de que ocurran problemas. Además, podemos utilizar AWS Config para rastrear cambios en la infraestructura y asegurarnos de que cumplan con nuestras políticas de seguridad y cumplimiento.

Este proceso automatizado de entrega continua nos permite desplegar rápidamente nuevas versiones de la aplicación de manera segura y confiable, garantizando una alta disponibilidad y confiabilidad para nuestros usuarios finales.
