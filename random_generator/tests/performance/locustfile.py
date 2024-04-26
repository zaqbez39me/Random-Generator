from locust import HttpUser, task


class MyUser(HttpUser):
    """
    Custom Locust user for simulating API requests.

    This user class defines tasks for simulating user behavior by sending
    GET requests to different endpoints.

    Example usage:
        user = MyUser()
        user.run()

    Tasks:
        weather_endpoint: Simulate a user accessing the weather endpoint.
        news_endpoint: Simulate a user accessing the news endpoint.
        time_endpoint: Simulate a user accessing the time endpoint.
    """

    @task
    def weather_endpoint(self) -> None:
        """
        Simulate a user accessing the weather endpoint.

        This task sends a GET request to the '/api/random/weather' endpoint
        using the client.
        """
        self.client.get("/api/random/weather")

    @task
    def news_endpoint(self) -> None:
        """
        Simulate a user accessing the news endpoint.

        This task sends a GET request to the '/api/random/news' endpoint
        using the client.
        """
        self.client.get("/api/random/news")

    @task
    def time_endpoint(self) -> None:
        """
        Simulate a user accessing the time endpoint.

        This task sends a GET request to the '/api/random/time' endpoint
        using the client.
        """
        self.client.get("/api/random/time")
