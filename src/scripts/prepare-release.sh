if [[ -z $1 ]]
then
    echo "No version argument was provided to \"prepare-release.sh\""
    exit 1
fi
echo "Writing \"$1\" to \"version.txt\""
echo $1 > ../version.txt
