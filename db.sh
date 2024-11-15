CONTAINER_TAG="latest"
CONTAINER_NAME="db"
USER_NAME="root"
PASSWORD="twentyone"
TARGET_DIR="db"

docker pull mysql/mysql-server:$CONTAINER_TAG
docker run --name=$CONTAINER_NAME -d --mount type=bind,source="$(pwd)"/$TARGET_DIR,target=/var/lib/mysql mysql/mysql-server:$CONTAINER_TAG 
until [ "$( docker container inspect -f '{{.State.Health.Status}}' $CONTAINER_NAME )" = "healthy" ]; do
    sleep 0.1;
done;