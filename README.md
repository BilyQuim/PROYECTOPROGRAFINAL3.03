# 🕯️ Sistema Integrado de Gestión de Inventarios y Auditoría - Cerería El Shaddai

## 📝 1. Descripción del Proyecto
Este sistema es una solución tecnológica empresarial distribuida, diseñada específicamente para automatizar el control de inventarios, el catálogo maestro de productos y la auditoría financiera de la **Cerería El Shaddai**. 

La plataforma resuelve problemas críticos de sincronización entre múltiples sucursales mediante el uso de transacciones electrónicas seguras. Al estar diseñada bajo una arquitectura de microservicios, garantiza que procesos pesados como la analítica gerencial o el historial de movimientos de inventario (**Kardex**) no congelen ni afecten las operaciones rutinarias de venta o mantenimiento del catálogo.

---

## 🏗️ 2. Arquitectura General del Sistema

El ecosistema está construido bajo el patrón de **Sistemas Distribuidos Modulares**, aislando las responsabilidades del negocio en contenedores independientes que se ejecutan sobre una red interna virtualizada. 

[ CLIENTE WEB (Front-end SPA) ] 
                 │
                 ▼ (Puerto 80: Tráfico HTTP)
     [ API GATEWAY (Traefik) ]
                 │
  ┌──────────────┼──────────────┐
  │ (Path /auth) │ (Path /rest) │ (Path /graphql)
┌───────────┐  ┌───────────┐  ┌───────────┐
│   Auth    │  │ Catálogo  │  │ Analítica │
│  Service  │  │ REST API  │  │  GraphQL  │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘
│              │              │
└──────────────┼──────────────┘
▼
[ REPOSITORIO DE DATOS ]
(MySQL 8.0)

### Componentes de la Infraestructura
* **Capa de Presentación (Frontend):** Interfaz de usuario construida como una **SPA (Single Page Application)** utilizando HTML5 estructurado, CSS3 con esteroides estéticos de **Bootstrap 5**, y un motor dinámico en **JavaScript Asíncrono** nativo (`async/await` y API Fetch) que actualiza la pantalla en tiempo real sin recargar el navegador.
* **API Gateway (Traefik):** Actúa como el único punto de contacto público del sistema. Administra el enrutamiento inteligente analizando los prefijos de las URLs entrantes para dirigir el tráfico de manera segura a la red interna de Docker (`cereria-network`).
* **Microservicio de Autenticación (`auth-service`):** Desarrollado en FastAPI. Valida las credenciales de los empleados y emite pasaportes de seguridad criptográficos basados en el estándar **JWT (JSON Web Tokens)** con algoritmo `HS256`.
* **Microservicio de Catálogo (`rest-service`):** Desarrollado en FastAPI. Encargado de las operaciones puras de mantenimiento físico de productos (CRUD) utilizando un diseño de arquitectura RESTful tradicional.
* **Microservicio de Negocio y Analítica (`graphql-service`):** Desarrollado en FastAPI utilizando la librería **Strawberry**. Expone un único endpoint flexible para resolver consultas financieras masivas y ejecutar operaciones transaccionales complejas.
* **Capa de Persistencia (MySQL 8.0):** Base de datos relacional centralizada. No solo guarda datos, sino que procesa lógica pesada interna a través de **Vistas** de agregación y **Procedimientos Almacenados** para asegurar la integridad total del Kardex.

---

## 🚀 3. Instrucciones para Ejecutar con Docker

Sigue estos pasos lógicos para compilar, configurar y levantar toda la infraestructura del sistema en cualquier entorno local en cuestión de segundos:

### Paso 1: Clonar y posicionarse en el proyecto
Abre tu terminal favorita, clona el repositorio o ingresa directamente a la carpeta raíz del proyecto:
```bash
cd "Ruta/De/Tu/Proyecto/Proyecto Final"
docker-compose up -d --build
docker-compose ps

Mapeo de Puertos Locales de la Red
Tras levantar los contenedores, el API Gateway expone y centraliza los accesos en las siguientes direcciones:

Panel Web del Frontend: http://localhost (Puerto default 80)

Dashboard de Traefik: http://localhost:8088

Gestor de Base de Datos (phpMyAdmin): http://localhost:8085

Entorno de Pruebas GraphQL (Strawberry Playground): http://localhost/graphql

📦 4. Endpoints del Microservicio REST (Catálogo)
GET	/rest/api/v1/rest/productos
POST	/rest/api/v1/rest/productos
PUT	/rest/api/v1/rest/productos/{id}
DELETE	/rest/api/v1/rest/productos/{id}

5. Queries y Mutations del Microservicio GraphQL (Strawberry)
Diseñado para romper con el esquema rígido de REST, este microservicio procesa consultas personalizadas de auditoría y operaciones complejas del Kardex en un solo endpoint (/graphql).

🔍 Queries (Consultas de Lectura de Datos)
A. verExistencias
query {
    verExistencias {
        IDStock
        IDSucursal
        IDProducto
        stockActual
    }
}
B. alertasStockBajo
query {
    alertasStockBajo {
        nombre_sucursal
        nombre_producto
        categoria
        stock_actual
    }
}
C. valorInventarioPorSucursal
query {
    valorInventarioPorSucursal {
        nombre_sucursal
        total_unidades
        valor_monetario_total
    }
}
A. crearProducto
mutation {
    crear_producto(nombre: "Vela Mágica Vainilla", categoria: "Aromáticas", costo: 18.50) {
        success
        message
    }
}
B. actualizarCostoProducto
mutation {
    actualizarCostoProducto(idProducto: 1, nuevoCosto: 14.70) {
        success
        message
    }
}
C. registrarMovimientoKardex
mutation {
    registrarMovimientoKardex(
        idProducto: 1,
        idSucursal: 1,
        idUsuario: 2,
        tipoMovimiento: "ENTRADA",
        cantidad: 10
    ) {
        success
        message
    }
}
👥 6. Usuarios y Credenciales de Prueba
Para interactuar de forma inmediata con las capas protegidas del sistema (escribir en REST o mutar en GraphQL), se ha inyectado un set de datos inicial (Seeding) en el contenedor de MySQL con el siguiente usuario operativo:

Nombre de Usuario (Login): carlos_encargado1

Contraseña Base: 123456

Rol del Sistema: Encargado de Inventario / Auditor de Sucursal