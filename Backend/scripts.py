import subprocess


def start_server_dev():
    subprocess.run("granian --interface asgi server/main:app --reload --port 6789")
