CONTAINER_TAG="latest"
CONTAINER_NAME="db"
USER_NAME="root"
PASSWORD="twentyone"
TARGET_DIR="db"

docker pull mysql/mysql-server:$CONTAINER_TAG

if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

docker run --name=$CONTAINER_NAME -d --mount type=bind,source="$(pwd)"/$TARGET_DIR,target=/var/lib/mysql mysql/mysql-server:$CONTAINER_TAG 
until [ "$( docker container inspect -f '{{.State.Health.Status}}' $CONTAINER_NAME )" = "healthy" ]; do
    sleep 0.1;
done;
TEMP_PASSWORD=$(docker logs $CONTAINER_NAME 2>&1 | grep GENERATED | awk '{print $5}')
# echo "PASSWORD: $TEMP_PASSWORD"
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$TEMP_PASSWORD -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$PASSWORD';" --connect-expired-password
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$PASSWORD -e "drop schema test;" --connect-expired-password


echo "Your mysql database has been setup successfully!"
echo "Container Name: $CONTAINER_NAME"
echo "User Name: $USER_NAME"
echo "Password: $PASSWORD"
echo "Target Directory: $TARGET_DIR"

echo "The database is accessible at localhost:3306, the password is $PASSWORD, and the data is stored in $(pwd)$TARGET_DIR."
echo "To run the databse, use the command 'source db.sh' in this directory."
echo "To stop the database, use the command 'source stop.sh' in this directory."
echo "Make sure you run stop.sh before you close docker or shut down your computer."