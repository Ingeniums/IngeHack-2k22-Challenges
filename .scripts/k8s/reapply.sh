#!/bin/sh

kubectl delete -f "$@"
kubectl apply -f "$@"
