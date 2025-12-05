# script for running om debiam based server or prod env

cd /home/admin/Task-Automation-API
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 &
celery -A worker worker --loglevel=info --pool=solo &
wait

