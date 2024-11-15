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
TEMP_PASSWORD=$(docker logs $CONTAINER_NAME 2>&1 | grep GENERATED | awk '{print $5}')
echo "PASSWORD: $TEMP_PASSWORD"
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$TEMP_PASSWORD -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$PASSWORD';" --connect-expired-password
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$PASSWORD -e "drop schema test; create schema test;" --connect-expired-password