import os

class Config():
    def __init__(self) -> None:
       
        self.DMP_AGENT_URL = os.getenv("DMP_AGENT_URL", "http://192.168.12.84:8520")
        # self.DMP_AGENT_URL = ("DMP_AGENT_URL", "http://127.0.0.1:8960")
        self.DMP_AGENT_USER_NAME = os.getenv("DMP_AGENT_USER_NAME", "admin")
        self.DMP_AGENT_PASSWORD = os.getenv("DMP_AGENT_PASSWORD", "040a201e60bfc745687103186b771bce90e5479c4e139b91f4c9ee5d77d487ff8b1aa72a81ff6553fbcac5ce24ff3857f47e6c344567cdd91b9d7dfa7fb553da0a08f94ac63c941ba688013fa9ac2f2576ca75532e92b7a6761284ae3b59fef1237158be4c0658b88358cdada989e8b03c")
