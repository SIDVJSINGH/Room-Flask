# Room-Flask

## Commands used to create the Docker image:

### Build the image:

```
docker build -t chatroom .
```

### Run the image:

```
docker run -p 5000:5000 chatroom
```

### Push to DockerHUB:

```
docker tag chatroom:latest <your_dockerhub_username>/chatroom:latest
```

#### For example my dockerhub username is:

```
sidvjsingh
```

```
docker tag chatroom:latest sidvjsingh/chatroom:1.0
```

```
docker push sidvjsingh/chatroom:1.0
```

## To Run the application on your local after installing Docker Desktop:

```
docker run -p 5000:5000 sidvjsingh/chatroom:1.0
```

##

# Application Manifest to run on Kubernetes Server

## Apply all the manifests:

```
kubectl apply -f chat-namespace.yml
kubectl apply -f chat-deployment.yml
kubectl apply -f chat-service.yml
```

## To view the service IP

```
kubectl get svc -n chat
```

## To view the Running Pods

```
kubectl get pods -n chat
```

## To view the complete logs of the running Pod

```
kubectl logs -f <POD_NAME> -n chat
```

# Terraform Commands
## Terraform INITIALIZE
```
terraform init 
```
## To reconfigure the backend
```
terraform init -reconfogure
```
## Terraform Plan
### To save the plan to use in apply command add ```-out=tfplan``` flag at the end
```
terraform plan -out=tfplan
```
## Terraform Apply
```
terraform apply
```
### To avoid writing yes each time add ```--auto-approve``` flag at the end
### To add planed out add ```"tfplan"``` at the end of the command
```
terraform apply --auto-approve "tfplan"
```
