from dotenv import dotenv_values

default_envs = {"debug": True}
config = {
    **default_envs,
    **dotenv_values(".env")
}
