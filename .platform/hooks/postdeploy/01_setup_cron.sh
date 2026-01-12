set -a
source /opt/elasticbeanstalk/deployment/env
set +a

VENV_PYTHON="/var/app/venv/*/bin/python"
PROJECT_DIR="/var/app/current"
LOG_FILE="/var/log/scryfall_cron.log"

crontab -u ec2-user - <<EOF
0 3 * * * cd $PROJECT_DIR && $VENV_PYTHON manage.py sync_scryfall_prices >> $LOG_FILE 2>&1
EOF