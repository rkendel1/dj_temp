PROJECT_ROOT=`dirname "$(readlink -f "$0")"`
CWD=$(pwd)
TEMPLATE=$1
echo "Will create a django project using $TEMPLATE template in $CWD/{project name}"
$PROJECT_ROOT/venv/bin/python $PROJECT_ROOT/djangotemplate.py $TEMPLATE
