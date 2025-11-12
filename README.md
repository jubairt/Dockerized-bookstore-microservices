# 🚀 Dockerized Microservices Setup (FastAPI + PostgreSQL + Prometheus)

This project demonstrates a complete **Dockerized microservices setup** using **FastAPI** for services, **PostgreSQL** for the database, and **Prometheus** for monitoring.

The focus of this README is on understanding and running the **Docker setup**, not on the application code itself.

---

## 🧩 Overview

Each microservice (User, Book, and Order) runs independently in its own container.  
All services connect to a shared PostgreSQL database container.  
Prometheus is also included for monitoring.

---

## 🐳 Docker Components

### **Services Defined in `docker-compose.yml`**
- **db (PostgreSQL)** — Main database service  
- **user_service** — Handles user management  
- **book_service** — Handles book records  
- **order_service** — Handles order management  
- **prometheus** — For monitoring the health of the services

---

## ⚙️ Docker Compose Configuration

Main commands are defined inside the `docker-compose.yml` file:

- Builds three FastAPI containers using their individual `Dockerfile`s.
- Connects all services through an internal Docker network.
- Uses a **persistent volume** for PostgreSQL data (`postgres_data`).

---

## 🗂️ Volumes and Persistence

A Docker volume named `postgres_data` ensures that PostgreSQL data remains safe even after containers are stopped or deleted.

To verify:
```bash
docker volume ls
```
Output should include something like:
```
my_project_postgres_data
```

The data is stored at:
```
/var/lib/docker/volumes/my_project_postgres_data/_data
```

Even if you stop or restart the container, your data will persist.

---

## 🪣 Automatic Database Setup with `init.sql`

This project uses an **`init.sql`** file to automatically create all required databases when the PostgreSQL container starts for the first time.  

### How it works:
- Place SQL commands (e.g., `CREATE DATABASE user_db;`) in `init.sql`.
- Mount it into the container at `/docker-entrypoint-initdb.d/`.
- PostgreSQL executes these scripts on first initialization.

### Example `docker-compose.yml`:

```yaml
db:
  image: postgres:15
  container_name: postgres_db
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: jubair
    POSTGRES_DB: book_db
  ports:
    - "5432:5432"
  volumes:
    - postgres_data:/var/lib/postgresql/data
    - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql

```
---

## ▶️ How to Start the Project

### **1️⃣ Build and Start Containers**
```bash
docker compose up -d --build
```

This command:
- Builds all images using their respective `Dockerfile`s
- Starts each service in detached mode (`-d`)

## 🧠 Verify Everything Works

### **Check Running Containers**
```bash
docker ps
```

### **Check PostgreSQL Connection**
```bash
docker exec -it postgres_db psql -U postgres
\c book_db
\dt   -- list tables
```

---

## 🧹 Stop and Clean Up

### **Stop Containers**
```bash
docker compose stop
```
This will stop containers but keep the data volume intact.

### **Remove Containers**
```bash
docker compose down
```
This stops and removes containers, but the `postgres_data` volume still persists.

### **Remove Everything (including volume)**
```bash
docker compose down -v
```
This removes containers **and** deletes the PostgreSQL volume (⚠️ data lost).

---

## 🔍 Check Volume and Data

To confirm the database data still exists:
```bash
docker volume inspect my_project_postgres_data
```

If you restart containers, your old data should still be available.

---

## ⚡ Prometheus Setup

Prometheus is configured to monitor all containers.  
Its configuration file is mounted using:
```yaml
volumes:
  - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
```

## 🔌 Service Ports

| Service        | Port (Host → Container) | Description                     |
|----------------|------------------------|---------------------------------|
| User Service   | 8001 → 8001            | Handles user management         |
| Book Service   | 8002 → 8002            | Handles book records            |
| Order Service  | 8003 → 8003            | Handles order management        |
| PostgreSQL DB  | 5432 → 5432            | Main database container         |
| Prometheus     | 9090 → 9090            | Monitoring all running services |


---

## 🧰 Useful Commands Summary

| Action | Command |
|--------|----------|
| Build and start everything | `docker compose up -d --build` |
| Start individual service | `docker compose up -d user_service` |
| Stop all containers | `docker compose stop` |
| Remove all containers | `docker compose down` |
| Remove everything including data | `docker compose down -v` |
| View running containers | `docker ps` |
| View logs | `docker logs <container_name>` |
| Enter container | `docker exec -it <container_name> bash` |
| Test DB connection | `docker exec -it postgres_db pg_isready -U postgres` |

---

## 🧾 Notes

- Make sure your `.env` files exist for each service.
- You can manually inspect PostgreSQL data anytime through the container.
- Volumes ensure that data remains safe even after container restarts.

---

## ✅ End-to-End Flow

1. Run `docker compose up -d --build`
2. Wait for PostgreSQL to start
3. Create databases (`book_db`, `user_db`, `order_db`)
4. Start remaining services
5. Access each service:
   - User Service → `localhost:8001`
   - Book Service → `localhost:8002`
   - Order Service → `localhost:8003`
6. Monitor metrics in Prometheus → `localhost:9090`

---

## 💡 Summary

This setup provides a **clean, production-ready Docker workflow**:
- Each service has its own isolated environment
- PostgreSQL data is persistent through Docker volumes
- Prometheus handles monitoring
- Everything can be built, started, or destroyed using simple Docker commands

---

✨ **That’s it! Your Dockerized microservice environment is ready to roll!**

