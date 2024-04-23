from locust import HttpUser, between, task

class MyUser(HttpUser):
    wait_time = between(0.001, 0.002)

    @task
    def weather_endpoint(self) -> None:
        self.client.get("/api/random/weather")

    @task
    def news_endpoint(self) -> None:
        self.client.get("/api/random/news")

    @task
    def time_endpoint(self) -> None:
        self.client.get("/api/random/time")
