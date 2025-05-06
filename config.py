import os

class Config():
    def __init__(self) -> None:
       
        self.DMP_AGENT_URL = os.getenv("DMP_AGENT_URL", "http://192.168.1.43:8960")
        # self.DMP_AGENT_URL = ("DMP_AGENT_URL", "http://127.0.0.1:8960")
        self.DMP_AGENT_USER_NAME = os.getenv("DMP_AGENT_USER_NAME", "admin")
        self.DMP_AGENT_PASSWORD = os.getenv("DMP_AGENT_PASSWORD", "04624b74ec268bdb0e292a79ecc7d4492d3ac140edcd6ed0d0122ec69d45f41f4861e950e981b2d5e43ae65ac47ed0f166ef97cf40b14afd346cacb4428ef0ed3087c52230aa3f5949488b76753265b994d8554e047c47ea15c9a2e1c06220687c1814ae132b694080f330c6e43b54d72b")
