[[ $1 =~ ^([^\/]+)\/([^\/,]+) ]]
FOLDERPATH="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
CORRECT=1
for i in $(echo $1 | tr "," "\n")
do
  [[ $i =~ ^([^\/]+)\/([^\/]+) ]]
  if [[ "${BASH_REMATCH[1]}/${BASH_REMATCH[2]}" != $FOLDERPATH ]]; then
    echo "There is more than one folder changed:"
    echo "Folder1: $FOLDERPATH"
    echo "Folder2: ${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    CORRECT=0
    exit 1
  fi
done

if [[ $CORRECT -eq 1 ]]; then
  echo "Only one folder changed"
fi
