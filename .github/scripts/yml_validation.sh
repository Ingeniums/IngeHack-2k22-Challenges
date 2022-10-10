[[ $1 =~ ^([^\/]+)\/([^\/,]+) ]]
FOLDERPATH="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"


if [ ! -f $FOLDERPATH/challenge.yml ]; then
    echo " .yml file is missing!"
    exit 1
fi

FILE=$FOLDERPATH/challenge.yml

if [[ -z $(grep "name" "$FILE") ]]; then echo "The challenge's name is missing"; exit 1; fi

if [[ -z $(grep "author" "$FILE") ]]; then echo "The challenge's author is missing"; exit 1; fi

if [[ -z $(grep "category" "$FILE") ]]; then echo "The challenge's category is missing"; exit 1; fi

if [[ -z $(grep "difficulty" "$FILE") ]]; then echo "The challenge's difficulty is missing"; exit 1; fi

if [[ -z $(grep "description" "$FILE") ]]; then echo "The challenge's description is missing"; exit 1; fi

if [[ -z $(grep "flags" "$FILE") ]]; then echo "The challenge's flag is missing"; exit 1; fi

echo "The challenge.yml file is valid"
