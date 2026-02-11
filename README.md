# 🐳FastAPI-K8s-App-Sistema-Distribuido-con-Minikube
<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/879eb896-5483-4630-8107-ee8ef797caa6" />
Este proyecto desarrolla una arquitectura de microservicios distribuida basada en FastAPI como framework principal, utilizando Redis para mensajería y caché, PostgreSQL como sistema de persistencia de datos y Nginx como proxy inverso y balanceador de carga. La solución se encuentra contenedorizada y orquestada en un clúster de Kubernetes (Minikube), garantizando escalabilidad, aislamiento de servicios y una gestión eficiente del tráfico y los recursos.

# 📦Componentes del sistema
| Componente        | Función                                                     |
|-------------------|-------------------------------------------------------------|
| **FastAPI + Uvicorn** | API stateless con endpoints `/` y `/db`                     |
| **Redis**         | Almacenamiento en caché y contador de visitas               |
| **PostgreSQL**    | Base de datos para persistencia                             |
| **Nginx**         | Balanceador de carga para múltiples réplicas                |

# 📁Estructura del proyecto
```text
fastapi_k8s_app/
├── app/
│   └── main.py              # Código de la API FastAPI
├── k8s/
│   ├── app.yaml             # Despliegue y servicio para FastAPI
│   ├── redis.yaml           # Redis deployment + service
│   ├── postgres.yaml        # PostgreSQL deployment + PV + service
│   └── nginx.yaml           # Configuración balanceador Nginx
├── Dockerfile               # Imagen personalizada para FastAPI
├── build_and_reload.sh      # Script de despliegue sin Docker Desktop
└── README.md                # Este archivo
```
# 🚀Cómo desplegar
# Requisitos:
- [ ] Docker Desktop (opcional)
- [x] Minikube
- [x] kubectl

Verificamos la instalación:

```bash
minikube version
kubectl version --client
```
# PASO 1 — Instalamos kubectl
Ejecutamos el siguiente comando para la instalacion:
```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
Luego damos permisos y agregamos al PATH:
```
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
```
Verificamos la version:
```
kubectl version --client
```
Si observamos una versión entonces todo está → ✅ listo.

# 🚀 PASO 2 — Instalamos Minikube

Ejecutamos el siguiente comando para el paquete:
```
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
```
Luego procedemos a la instalación:
```
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
Verificamos la versión:
```
minikube version
```
Debe mostrar todas la verciones → ✅ listo.
```
docker --version
minikube version
kubectl version --client
```
## Iniciar el cluster
```
minikube start --driver=docker
```
Luego verificas que esté funcionando:
```
kubectl get nodes
```
Eso levanta Kubernetes usando Docker.

## 1.Inicia Minikube
```
minikube start
```
## 2. Construye la imagen dentro de Minikube
```
minikube image build -t fastapi-app:latest .
```
💡 Si usas Docker Desktop y no estás en entorno multinodo, puedes usar:
```
docker build -t fastapi-app:latest .
minikube image load fastapi-app:latest

```
## 3. Despliega todos los recursos de Kubernetes
```
kubectl apply -f k8s/
```
Esto crea:
- Deployments
- Services
- Configuración de Nginx

## 4. Verifica el estado de los Pods
```
kubectl get pods
```
## 5.  Obtén la URL pública para acceder a la app
```
minikube service nginx --url
```
Accede desde el navegador usando la URL generada.
## 📬 Endpoints disponibles

| <small>Método</small> | <small>Endpoint</small> | <small>Descripción</small> |
|---------------------------|------------------------|----------------------------|
| GET                       | /                      | Retorna mensaje y contador de visitas almacenado en Redis.    |
| GET                       | /db                    | Ejecuta las tareas         |

## 🔄 Escalabilidad y tolerancia a fallos
**Escalar horizontalmente**
```
kubectl scale deployment fastapi-app --replicas=5
```
Esto crea múltiples instancias de la API.

## 💥 Simular caída de una réplica
```
kubectl delete pod <nombre-del-pod>
```
Kubernetes recreará automáticamente el pod eliminado.
Nginx continuará balanceando entre las réplicas disponibles.

## 🛡️ Pruebas de Resiliencia

Estas pruebas permiten validar la tolerancia a fallos y el comportamiento del sistema ante interrupciones.

## 🔧 Opción A – Simular caída de NGINX (Pod)
```
kubectl delete pod -l app=nginx
```
Esto simula una falla inesperada. Kubernetes automáticamente levantará un nuevo pod gracias al Deployment.
Monitorear recreación:
```
kubectl get pods -l app=nginx -w
```
✅ Recomendado para probar auto-recuperación sin perder el recurso de servicio.

## 🔧 Opción B – Escalar NGINX a 0 (simular mantenimiento)
```
kubectl scale deployment nginx --replicas=0
```
Restaurar servicio:
```
kubectl scale deployment nginx --replicas=1
```
🔁 Útil para mantenimiento controlado.

## ❌ Opción NO recomendada – Eliminar el servicio de NGINX
```
kubectl delete svc nginx
```
⚠️ Esto elimina el balanceador de carga y la URL pública de Minikube dejará de funcionar. Solo usar si deseas reconfigurar el servicio desde cero.

## 🧪 Recomendaciones de prueba

- Ejecutar pruebas con múltiples réplicas activas.
- Verificar que la API responde tras recuperación.
- Usar **curl** o navegador para observar interrupciones mínimas.
- Monitorear pods en tiempo real:
```
kubectl get pods -w
```
## 🧼 Limpieza

Eliminar todos los recursos creados:
```
kubectl delete -f k8s/
```
Opcionalmente detener Minikube:
```
minikube stop
```
# 👨‍💻 Autor
**Leider Samudio** - DevOps & Cloud Enthusiast

<small>[GitHub: @jcontreras-dev](https://github.com/jcontreras-dev)</small>






















  
















