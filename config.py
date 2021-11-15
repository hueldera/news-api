from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DJANGO",
    settings_files=["settings.yaml", ".secrets.yaml"],
    environments=True,
    load_dotenv=True,
)
