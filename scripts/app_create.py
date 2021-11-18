from app_config import AppConfig
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from tqdm.auto import tqdm

CONFIG = AppConfig()


class LuisApp():
    def __init__(self):
        self.client = self.create_client()
        self.auth_client = self.create_auth_client()
        self.app_id = None,
        self.app_version = None

    def create_client(self):
        return LUISRuntimeClient(
            CONFIG.LUIS_ENDPOINT,
            CognitiveServicesCredentials(CONFIG.LUIS_API_KEY),
        )

    def create_auth_client(self):
        return LUISAuthoringClient(
            CONFIG.AUTHORING_ENDPOINT,
            CognitiveServicesCredentials(CONFIG.AUTHORING_KEY),
        )

    def create_luis_app(self, name="TravelApp", version="0.1", description="FlyMe Luis App", culture="en-us"):
        app_name = name
        app_version = version
        app_description = description
        app_culture = culture

        # Call the details
        app_id = self.auth_client.apps.add(dict(
            name=app_name,
            initial_version_id=app_version,
            description=app_description,
            culture=app_culture))

        print('Created LUIS app {}  with ID "{}"'.format(name, app_id))
        self.app_id = app_id
        self.app_version = app_version
        return app_id, app_version

    def create_luis_intents(self):
        bar1 = tqdm(
            total=(len(CONFIG.INTENTS)),
            position=0,
            dynamic_ncols=True,
            leave=True,
            unit="",
            desc="Creating intents",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]"
        )
        for intent in CONFIG.INTENTS:
            self.auth_client.model.add_intent(self.app_id, self.app_version, intent)
            bar1.update(int(1))

    def create_luis_entities(self):
        bar1 = tqdm(
            total=(len(CONFIG.ENTITIES) + 1),
            position=0,
            dynamic_ncols=True,
            leave=True,
            unit="",
            desc="Creating entities",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]"
        )
        for entity in CONFIG.ENTITIES:
            self.auth_client.model.add_entity(self.app_id, self.app_version, name=entity)
            bar1.update(int(1))
        for entity in CONFIG.PREBUILT_ENTITIES:
            self.auth_client.model.add_prebuilt(self.app_id, self.app_version, prebuilt_extractor_names=[entity])
            bar1.update(int(1))

    def publish_app(self):
        self.auth_client.apps.update_settings(self.app_id, is_public=True)
        response = self.auth_client.apps.publish(
            self.app_id,
            self.app_version,
            is_staging=False)

        print('App is published. Endpoint : ', response.endpoint_url)
