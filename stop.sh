CONTAINER_TAG="latest"
CONTAINER_NAME="db"
USER_NAME="root"
PASSWORD="twentyone"
TARGET_DIR="db"

docker stop $CONTAINER_NAME
docker remove $CONTAINER_NAME

echo "Your mysql database has been stopped successfully!"