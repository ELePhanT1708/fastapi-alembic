from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host = 'http://localhost:8000'

    @task
    def get_operations(self):
        self.client.get("/operations/?operation_type=casual")
