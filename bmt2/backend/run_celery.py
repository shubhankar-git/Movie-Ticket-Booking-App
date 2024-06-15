import subprocess
import os

app_directory =  os.path.dirname(os.path.abspath(__file__))
# Command to run the Celery worker

worker_command = f"celery -A my_celery worker --loglevel=info"

# Command to run the Celery beat
beat_command = f"celery -A my_celery beat --loglevel=info"

flower_command= f"celery -A my_celery flower"

# Run the Celery worker and beat tasks using subprocess

subprocess.Popen(worker_command, shell=True, cwd=app_directory)
subprocess.Popen(beat_command, shell=True, cwd=app_directory)
subprocess.Popen(flower_command, shell=True, cwd=app_directory)

file_path = os.path.join(app_directory, "celerybeat-schedule")  

# Check if the file exists before attempting to delete it
if os.path.exists(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting file: {e}")
else:
    print(f"File '{file_path}' does not exist.")

#     celery -A my_celery worker --loglevel=info
#     celery -A my_celery beat --loglevel=info
#         celery -A my_celery flower