
# twitter insight k8s service 📝  
The Twitter data processing application is designed to process and analyze Twitter data, providing insights into tweet distributions by author, sentiment analysis, and more. The application is containerized and designed to run within a Kubernetes environment, ensuring scalability and ease of deployment.

## Get Started 🚀  
we are using minikube to run the k8s cluster

## Install minikube 🛠️
```sh
pip install minikube/brew install minikube
```

## start minikube 🌟
```sh
minikube start
```

## enable ingress 🖌️
```sh
minikube addons enable ingress
```

### Create namespace

Create namespace for the k8s resources

```sh
kubectl create namespace twitty
```

### Create deployments

Create deployments and volumes

```sh
kubectl apply -f ./k8s -n twitty
```

## Access the frontend 🌐

Enable port forwarding

you can track the deployment with the minikube dashboard (`minikube dashboard`) or via kubectl.
to access the service go port forwarding...or go ingress, in which case:
- go `minikube tunnel` to allow ingress calls into minikube to happen on yr 127.0.0.1.
- edit yr hosts file (`/etc/hosts` on unixlikes) and add `127.0.0.1 twitty.com`

the UI should be available via `http://twitty.com` in yr browser.

## Usage 📊
option 1: Enter an authors name in the input box and press the button to recive a graph showing the distribution of the sentiment of their tweets
option 2: press the second button to recive a graph of the amount of tweets by all authors
option 3: Top Tweets by Likes and Shares
option 4: Top 10 Users by Content Volume
option 4: Analysis Based on Token - Enter tokens the analysis will be based on the table that partiotined by word


## Cleanup

Delete the namespace

```sh
kubectl delete namespace twitty
minikube stop
minikube delete
```
