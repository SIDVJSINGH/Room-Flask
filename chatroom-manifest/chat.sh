kubectl apply -f chat-namespace.yml
kubectl apply -f chat-deployment.yml
kubectl apply -f chat-service.yml

# To view the service IP
kubectl get svc -n chat

# To view the Running Pods
kubectl get pods -n chat

# To view the logs of the running Pods
kubectl logs -f <POD_NAME> -n chat