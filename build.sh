#!/bin/bash

if [ "$1" == "--help" ] || [ "$1" == "-h" ]; then
  echo "Usage: ./build.sh <image-name> <container-name> <port>"
  exit 0
fi

imgName=$1

if [ -z "$imgName" ]; then
  echo "Please provide image name"
  exit 1
fi

containerName=$2

if [ -z "$containerName" ]; then
  echo "Please provide container name"
  exit 1
fi

setPort=$3

if [ -z "$setPort" ]; then
  echo "Please provide port"
  exit 1
fi

export FUNNEL_PORT=$setPort

docker container rm -f $containerName

docker image rm -f $imgName

docker build -t $imgName .

docker run -d -p $setPort:$setPort --name $containerName --restart always $imgName