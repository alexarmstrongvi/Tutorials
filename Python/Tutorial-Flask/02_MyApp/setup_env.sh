# Configuration
APP_NAME="myapp.py" # assumed to be in same file as this setup script

# Setup
proj_dir="$(cd $(dirname ${BASH_SOURCE}) && pwd -P)"

export FLASK_APP="${proj_dir}/${APP_NAME}"
export FLASK_ENV="development"

# Summarize
echo "FLASK_APP : ${FLASK_APP}"
echo "FLASK_ENV : ${FLASK_ENV}"
echo "Run the application with 'flask run'"
echo "and then connect to generated URL in your browser"
