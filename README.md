# FastAPI Trade Order System

A FastAPI-based trading system that allows users to place, retrieve, and track stock orders in real-time using WebSockets. The application is containerized with Docker and deployed on AWS EC2 via GitHub Actions CI/CD.


Hosted at : http://3.93.163.119:8000/orders
---

## Features
- Create Orders - Users can place stock buy/sell orders.
- Retrieve Orders - View all existing trade orders.
- Real-Time Updates - WebSocket integration for real-time order tracking.
- Dockerized Deployment - Fully containerized using Docker & Docker Compose.
- CI/CD Pipeline - Automated deployment on AWS EC2 using GitHub Actions.
- Swagger API Docs - Interactive API documentation via OpenAPI.

---

## Tech Stack
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL (Hosted on NeonDB)
- **Containerization:** Docker, Docker Compose
- **Deployment:** AWS EC2 (Ubuntu)
- **CI/CD:** GitHub Actions
- **Real-Time Updates:** WebSockets

---

## API Documentation
Swagger UI is enabled by default. Once running, access API docs at:
- Swagger UI: `[http://<EC2-IP>:8000/docs](http://3.93.163.119:8000/docs)`
- ReDoc: `[http://<EC2-IP>:8000/redoc](http://3.93.163.119:8000/redoc)`

Swagger:
![image](https://github.com/user-attachments/assets/a19e11a9-b0cb-42bc-ae40-5e3e8647931f)

Redoc:
![image](https://github.com/user-attachments/assets/75c249ed-a6de-4919-954b-bbdd40d34856)


---

## Getting Started

### Clone the Repository
```sh
git clone https://github.com/sailesh2710/FastAPI_Trade.git
cd FastAPI_Trade
```

### Create a Virtual Environment & Install Dependencies
```sh
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
pip install -r requirements.txt
```
### Set Up Environment Variables
Create a .env file inside the project and add the database connection:
```sh
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
```
### Run the Application Locally
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
Open http://127.0.0.1:8000/docs to test the API.

---

## Docker Setup
### Build & Run Docker Container
```sh
docker build -t fastapi-trade-app .
docker run -d -p 8000:8000 --env-file .env --name fastapi-trade-app fastapi-trade-app
```
### Using Docker Compose
If you have docker-compose.yml, simply run:
```sh
docker-compose up --build -d
```

---

## WebSocket Integration
To receive real-time order updates, use this WebSocket connection (also attached in repository):
```sh
import asyncio
import websockets

async def listen():
    async with websockets.connect("ws://<EC2-IP>:8000/ws/orders") as websocket:
        while True:
            message = await websocket.recv()
            print(f"New Order Received: {message}")

asyncio.run(listen())
```

---

## Deployment on AWS EC2

This application is deployed on AWS EC2 using GitHub Actions CI/CD.
### Deploy Manually on EC2
- SSH into the EC2 instance:
```sh
ssh -i "your-key.pem" ubuntu@<EC2-IP>
```
- Pull & Run Docker Image:
```sh
sudo docker pull sailesh2710/fastapi-trade-app:latest
sudo docker run -d -p 8000:8000 --env DATABASE_URL=<database-url> --name fastapi-trade-app sailesh2710/fastapi-trade-app:latest
```

---

## Automated Deployment via GitHub Actions

- **CI/CD Pipeline Steps:**
  - Run tests on PRs.
  - Build and push Docker image to Docker Hub.
  - SSH into EC2 and deploy the latest version.

- **GitHub Secrets Required:**

| Secret Name       | Description                     |
|------------------|---------------------------------|
| `DOCKER_USERNAME` | Docker Hub username           |
| `DOCKER_PASSWORD` | Docker Hub password           |
| `EC2_HOST`       | AWS EC2 public IP             |
| `EC2_USER`       | SSH user (`ubuntu`)           |
| `EC2_SSH_KEY`    | Private SSH key for EC2       |
| `DATABASE_URL`   | PostgreSQL connection URL     |

---

## API Endpoints

| Method  | Endpoint   | Description           |
|---------|-----------|-----------------------|
| **POST** | `/orders` | Create a new order   |
| **GET**  | `/orders` | Retrieve all orders  |
| **WebSocket**  | `/ws/orders` | Real-time updates for new orders  |

Example cURL request to create an order:
```sh
curl -X 'POST' 'http://<EC2-IP>:8000/orders' \
  -H 'Content-Type: application/json' \
  -d '{
    "symbol": "AAPL",
    "price": 150.5,
    "quantity": 10,
    "order_type": "buy"
  }'
```

---

## Steps to Set Up CI/CD with GitHub Actions

### Step 1: Configure GitHub Secrets

Go to GitHub Repository → Settings → Secrets and Variables → Actions and add the following secrets:
- DOCKER_USERNAME
- DOCKER_PASSWORD
- EC2_HOST
- EC2_USER
- EC2_SSH_KEY
- DATABASE_URL

### Step 2: Create .github/workflows/deploy.yml
Initialise docker image actions in github repositiry and use the code from .github/workflows/deploy.yml.

---

## Future Improvements

- Implement authentication and authorization for API security.
- Add more detailed logging and monitoring.
- Enhance the WebSocket feature with better error handling and reconnection logic.
- Optimize database queries for performance improvements.
- Deploy a frontend to interact with the FastAPI backend.

---
## Contact
For any inquiries or support, feel free to reach out:

- **GitHub:** [@sailesh2710](https://github.com/sailesh2710)
- **Email:** saileshkumar2710@gmail.com

