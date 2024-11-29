CONTAINER_TAG="latest"
CONTAINER_NAME="db"
USER_NAME="root"
PASSWORD="twentyone"
TARGET_DIR="db"

echo -e "\033[1mPulling the mysql image...\033[0m"
docker pull mysql/mysql-server:$CONTAINER_TAG

if [ ! -d "$TARGET_DIR" ]; then
    mkdir -p "$TARGET_DIR"
fi

# docker run --name=$CONTAINER_NAME -d -p 3306:3306 mysql/mysql-server:$CONTAINER_TAG
echo -e "\033[1mRunning the mysql container... This may take a while.\033[0m" 
docker run --name=$CONTAINER_NAME -d -p 3306:3306 --mount type=bind,source="$(pwd)"/$TARGET_DIR,target=/var/lib/mysql mysql/mysql-server:$CONTAINER_TAG 
until [ "$( docker container inspect -f '{{.State.Health.Status}}' $CONTAINER_NAME )" = "healthy" ]; do
    sleep 0.1;
done;
TEMP_PASSWORD=$(docker logs $CONTAINER_NAME 2>&1 | grep GENERATED | awk '{print $5}')
# echo "PASSWORD: $TEMP_PASSWORD"

echo "Setting the defaults..."
echo -e "\033[1mSetting the defaults...\033[0m" 
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$TEMP_PASSWORD -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$PASSWORD';" --connect-expired-password
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$PASSWORD -e "CREATE USER 'root'@'%' IDENTIFIED BY '$PASSWORD';" --connect-expired-password
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$PASSWORD -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';" --connect-expired-password
docker exec $CONTAINER_NAME mysql -u$USER_NAME -p$PASSWORD -e "FLUSH PRIVILEGES;" --connect-expired-password

echo -e "\033[1mTrying to setup the database tables...\033[0m"
python -c "import mysql"
if [ $? -ne 0 ]; then
    echo -e "\033[1mThe mysql package is not installed in your current environment. Please install it using 'pip install mysql'.\033[0m"
    echo -e "\033[1mYou can setup the database tables manually by running 'python -m db' in this directory with the mysql package installed.\033[0m"
else 
    python -m db
    echo -e "\033[1mDatabase tables have been setup successfully!\033[0m"
fi

echo ""
echo "Your mysql database has been setup successfully!"
echo "Container Name: $CONTAINER_NAME"
echo "User Name: $USER_NAME"
echo "Password: $PASSWORD"
echo ""
# echo "Target Directory: $TARGET_DIR"

echo "The database is accessible at localhost:3306, the password is $PASSWORD, and the data is stored in $(pwd)/$TARGET_DIR. \n"
# echo "The database is accessible at localhost:3306, the password is $PASSWORD, and data is lost when the container is stopped."
echo "To run the databse, use the command 'source db.sh' in this directory."
echo "To stop the database, use the command 'source stop.sh' in this directory."
echo "Make sure you run stop.sh before you close docker or shut down your computer."