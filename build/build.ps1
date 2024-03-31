# windows because it might be necessary.
if ($args[0] -eq "--help" -or $args[0] -eq "-h") {
    Write-Host "Usage: .\build.ps1 <image-name> <container-name> <port>"
    exit 0
}

$imgName = $args[0]
if (-z $imgName) {
    Write-Host "Please provide image name"
    exit 1
}

$containerName = $args[1]
if (-z $containerName) {
    Write-Host "Please provide container name"
    exit 1
}

$setPort = $args[2]
if (-z $setPort) {
    Write-Host "Please provide port"
    exit 1
}

$env:FUNNEL_PORT = $setPort

docker container rm -f $containerName

docker image rm -f $imgName

docker build -t $imgName .

docker run -d -p $setPort:$setPort --name $containerName --restart always $imgName
