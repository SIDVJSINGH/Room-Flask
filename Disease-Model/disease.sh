kubectl apply -f model-ns.yml
kubectl apply -f model-deployment.yml
kubectl apply -f model-service.yml

kubectl apply -f frontend-deployment.yml
kubectl apply -f frontend-service.yml

# sleep 30

kubectl get svc -n backend