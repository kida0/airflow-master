FRUIT=$1

if [ $FRUIT = APPLE ]; then
        echo "Hi Apple!"
elif [ $FRUIT = ORANGE ]; then
        echo "Hi Orange!"
elif [ $FRUIT = GRAPE ]; then
        echo "Hi Grape!"
else
        echo "Hi Nothing!"
fi
