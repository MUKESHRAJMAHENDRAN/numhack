import os
from modal import Image, Secret, Stub, wsgi_app

image = (
    Image.debian_slim(python_version="3.11")
        .pip_install_from_requirements("requirements.txt")
        .copy_local_dir('chatapp', '/root/chatapp')
        .copy_local_dir('chatbot', '/root/chatbot')
        .copy_local_file('manage.py', '/root/chatbot/manage.py')
        .run_commands(
            "python /root/manage.py migrate",
            secrets=[Secret.from_name("my-app-secret")],
        )
)

stub = Stub(name="my-app", image=image)

@stub.function(
        secret=Secret.from_name("my-app-secret"),
        gpu="T4",
        concurrency_limit=1,
        container_idle_timeout=300,
    )
@wsgi_app()
def run():
    from chatbot.wsgi import application
        return application