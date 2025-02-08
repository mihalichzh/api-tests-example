import os


class Config:
    @staticmethod
    def get_env_var_or_throw(var_name: str) -> str:
        try:
            return os.environ[var_name]
        except KeyError:
            raise MissingEnvironmentVariable(
                f"'{var_name}' environment variable is missing"
            )

    @staticmethod
    def api_base_url() -> str:
        return Config.get_env_var_or_throw("API_BASE_URL")

    @staticmethod
    def api_key() -> str:
        return Config.get_env_var_or_throw("API_KEY")


class MissingEnvironmentVariable(Exception):
    pass
