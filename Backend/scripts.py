import subprocess


def start_server_dev():
    subprocess.run("granian --interface asgi server/main:app --reload --port 6789")


def start_server_prod():
    subprocess.run("granian --interface asgi server/main:app --port 6789")


def start_test_web_selenium():
    subprocess.run("poetry run pytest test/test_selenium.py -v")
