
# twitter insight k8s service 📝  
The Twitter data processing application is designed to process and analyze Twitter data, providing insights into tweet distributions by author, sentiment analysis, and more. The application is containerized and designed to run within a Kubernetes environment, ensuring scalability and ease of deployment.

## Get Started 🚀  
we are using minikube to  run the k8s cluster

## Install minikube 🛠️
```sh
pip install minikube/brew install minikube
```

## start minikube 🌟
```sh
minikube start
```

### Create the pods 📦
```sh
kubectl apply -f .\postgres.yaml
```
use kubectl get pods to ensure that postgress is running
```sh
kubectl get pods
```

run the rest of the pods
```sh
kubectl apply -f .\data_digest.yaml
kubectl apply -f .\frontend.yaml
kubectl apply -f .\data_analysis.yaml
```

## Access the frontend 🌐

to access the frontend and interact with the application run the following:
```sh
minikube service frontend-service to access
```

## Usage 📊
Enter an authors name in the input box and press the button to recive a graph showing the distribution of the sentiment of their tweets

press the second button to recive a graph of the amount of tweets by all authors


## Cleanup 🧹

to delete all resources run the following:

```sh
minikube stop
minikube delete
```
