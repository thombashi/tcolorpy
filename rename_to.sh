#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Usage: rename_to.sh NEW_NAME" 2>&1
fi

new_name=$1

sed -i -e "s/<project_name>/${new_name}/g" *.{ini,py,rst,toml}
sed -i -e "s/project_name/${new_name}/g" *.{ini,py,rst,toml} **/*.py
sed -i -e "s/python-lib-project-template/${new_name}/g" *.{ini,py,rst,toml}
mv project_name "${new_name}"
