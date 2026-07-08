#!/bin/bash

DEPLOYMENT="deployment.yaml"
SERVICE="service.yaml"

#verifica se o minikube está instalado e rodando
if command -v minikube >/dev/null 2>&1; then
    echo "Verificando se o minikube está rodando..."
    if ! minikube status | grep -q "Running"; then
        echo "Minikube não está rodando. Iniciando o minikube..."
        minikube start
    else
        echo "Minikube já está rodando."
    fi
else
    echo "Minikube não está instalado. Por favor, instale o minikube"
fi

echo "aplicando o deployment..."
kubectl apply -f $DEPLOYMENT 

echo "aplicando o service..."
kubectl apply -f $SERVICE

echo "Aguarde alguns segundos para que o serviço seja iniciado..."
kubectl wait --for=condition=available --timeout=60s deployment/livros-api

echo "iniciando port-forwarding para o localhost na porta 8000... -> service na porta 80"

#rodar o port-forwarding em background
kubectl port-forward svc/livros-api-service 8000:80 > /dev/null 2>&1 &

#espera alguns segundos para que o port-forwarding seja iniciado
sleep 3

# detecta o sistema operacional para abrir o navegador
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://localhost:8000
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://localhost:8000
elif [[ "$OSTYPE" == "cygwin" ]]; then
    cygstart http://localhost:8000
elif [[ "$OSTYPE" == "msys" ]]; then
    start http://localhost:8000
elif [[ "$OSTYPE" == "win32" ]]; then
    start http://localhost:8000
else
    echo "Sistema operacional não suportado. Por favor, abra o navegador manualmente e acesse http://localhost:8000"
fi

echo "aplicação está rodando em http://localhost:8000"
echo "Pressione Ctrl+C para parar o port-forwarding e encerrar o script."

#mantém o script em execução para que o port-forwarding continue ativo
wait


