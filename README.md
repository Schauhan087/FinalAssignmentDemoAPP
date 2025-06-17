Kubernetes Multi-Tier Application
Overview
Simple 3-tier web app: Frontend (Nginx) → Backend (Flask) → Database (MySQL)
Quick Setup
bash# Start cluster
minikube start

# Deploy everything
kubectl apply -f db/
kubectl apply -f backend/
kubectl apply -f frontend/

# Build backend image
cd backend
docker build -t my-flask-app:latest .
minikube image load my-flask-app:latest
cd ..

# Check status
kubectl get pods
kubectl get svc

# Access app
minikube service frontend-service --url
Project Structure
k8s-assignment/
├── README.md
├── frontend/     # Nginx + ConfigMap + NodePort
├── backend/      # Flask + ClusterIP + Secret
├── db/           # MySQL + PVC + Secret
└── screenshots/  # Required screenshots