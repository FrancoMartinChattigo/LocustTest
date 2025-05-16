from locust import HttpUser, task, between
from accounts import Accounts
from queue import Queue
from commons_qa_back.api.bff.api_bff_portal_login import ApiBFFPortalLogin
from commons_qa_back.api.bff.api_bff_chattigo_internal import ApiBFFChattigoInternal
import os
import random
import json

class MyUser(HttpUser):
    # colocamos el ambiente correspondiente
    os.environ.setdefault("env", "support-bugs")
    wait_time = between(1, 5)
    users_to_use = []
    for index, value in enumerate(range(2)):
        users_to_use.append(Accounts.get_account(f"agente_{index}"))

        print(f"Índice: {index}, Valor: {value}")
    #print(f"{users_to_use_dict}")
    host = f"https://{os.environ['env']}.chattigo.com/"
    user_queue = Queue()
    for user in users_to_use:
        user_queue.put(user)

    def on_start(self):
        # Seleccionar un agente aleatorio (agente_1 a agente_2)



        # Inicializar API
        #print(users_to_use)
        self.api_bff_chattigo_internal = ApiBFFChattigoInternal(self.account)
        self.info_chats = self.api_bff_chattigo_internal.get_inbox_internal_chats()
        print(self.api_bff_chattigo_internal.account, "header api bff")
        #print(self.info_chats, "info_chats")
        team_name = 'load team'
        self.group_id = [group.get('idChat') for group in self.info_chats['chatsInfo']
                          if team_name in group.get('groupName') ]
        print(self.group_id, "<<< ----- | ID del grupo")
        if len(self.group_id) == 0:
            assert False, f"no hay grupo llamado {team_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_bff_chattigo_internal.headers['Authorization']}",
            "Content-Type": "application/json",  # Asegúrate de incluir el Content-Type para JSON
            "Custom-Header": "valor-header",
            "Cookie": f"{self.api_bff_chattigo_internal.headers['Cookie']}"
        }
        print(self.headers)
    @task
    def test_send_chat_internal_outbound(self):
        # Define el cuerpo de la solicitud POST

        payload = {
            "idChat": self.group_id[0] ,  # Reemplaza con un chat_id real de tu sistema
            "content": "Este es un mensaje de prueba desde Locust"
            # Agrega otros campos necesarios según la API
        }
        print(payload)
        response = self.client.post(
            "bff-chattigo-internal/api/rest/v1/message/outbound",
            headers=self.headers,
            json=payload
        )

        print(f"Respuesta recibida: {response.text} , >>>", response)