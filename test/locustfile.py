from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    #Temps d'attente entre chaque requête (en secondes)
    wait_time = between(1, 3)
 
    @task
    def compute(self):
        self.client.get("/compute")

    @task
    def io(self):
        self.client.get("/io")

    @task
    def status(self):
        self.client.get("/status")



