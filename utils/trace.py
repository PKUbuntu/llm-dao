from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
from langchain_core.runnables import RunnableConfig

# langfuse = Langfuse(
#     public_key="pk-lf-11eb2a40-0d4c-4f24-afd5-f3d0dfc8943c",
#     secret_key="sk-lf-8b6d30a1-d69d-49d7-9b04-5dd7a8f4c3b0",
#     host="https://us.cloud.langfuse.com"
# )

langfuse = Langfuse(
    public_key="pk-lf-76649eae-bd1f-423a-b284-b8bc5c7626e7",
    secret_key="sk-lf-f2061e97-6801-4e33-bf4c-9b28181b268e",
    host="http://localhost:3000"
)

langfuse_handler = CallbackHandler()
config = RunnableConfig(callbacks=[langfuse_handler])