from locust import HttpUser, task, between
from accounts import Accounts
from commons_qa_back.api.bff.api_bff_portal_login import ApiBFFPortalLogin
from dotenv import load_dotenv
import os

class MyUser(HttpUser):
    wait_time = between(1, 5)
    host = "https://support-bugs.chattigo.com"  # <- Lo asignás acá

    def on_start(self):

        # - logeamos el usuario correspondiente que vamos a utilizar -

        os.environ.setdefault("env", "support-bugs")
        self.account = Accounts.get_account("agente_1")
        print("--- ",self.account.__dict__)
        self.api_bff_portal_login = ApiBFFPortalLogin(self.account)
        print(self.api_bff_portal_login.login())

        self.headers = {
            "Authorization": f"Bearer {self.api_bff_portal_login}",
            "Custom-Header": "valor-header"
        }

    @task
    def test_endpoint_with_header(self):
        self.client.get(
            "bff-chattigo-internal/api/rest/v1/message/outbound",
            headers=self.headers
        )
