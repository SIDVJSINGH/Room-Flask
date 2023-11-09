# gcloud config set project stp-7thsem

# Connecting to the cluster
gcloud container clusters get-credentials primary --zone us-central1 --project stp-7thsem


# Running the application with all manifests
kubectl apply -f chat-namespace.yml
kubectl apply -f chat-deployment.yml
kubectl apply -f chat-service.yml

sleep 180
# To view the service IP
kubectl get svc -n chatroom

# To view the Running Pods
# kubectl get pods -n chat

# To view the logs of the running Pods
# kubectl logs -f <POD_NAME> -n chat