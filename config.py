from dotenv import dotenv_values

default_envs = {"user_id": 1, "steps": 10, "model_id": "SD35LT", "debug": True}
config = {
    **default_envs,
    **dotenv_values(".env")
}
