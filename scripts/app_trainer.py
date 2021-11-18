import json
import random
import time

from app_config import AppConfig
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from tqdm.auto import tqdm

from helpers import *

CONFIG = AppConfig()

TEST_SIZE = 0.1
client = LUISAuthoringClient(
    CONFIG.AUTHORING_ENDPOINT,
    CognitiveServicesCredentials(CONFIG.AUTHORING_KEY),
)

pred_client = LUISRuntimeClient(
    CONFIG.LUIS_ENDPOINT,
    CognitiveServicesCredentials(CONFIG.LUIS_API_KEY),
)


class AppTrainer():
    def __init__(self, app_id, app_version):
        self.client = self.create_client()
        self.auth_client = self.create_auth_client()
        self.app_id = app_id
        self.app_version = app_version
        self.utterances = None
        self.test_sample = None

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

    def start_training(self, filename):
        if filename is None:
            filename = "./frames.json"
        with open(filename) as frames_file:
            data = json.load(frames_file)
        utterances = self.parse_file(data)
        print("Splitting train/test before training")
        self.utterances = utterances[0:160] + self.build_other_utterances()
        sample_size = round(len(self.utterances) * TEST_SIZE)
        random.shuffle(self.utterances)
        self.test_sample = self.utterances[:sample_size]
        self.utterances = self.utterances[sample_size:]
        self.send_batches(self.utterances)
        self.train_app()

    def train_app(self):

        print("\nApp in training")

        async_training = self.auth_client.train.train_version(
            self.app_id, self.app_version
        )
        is_trained = async_training.status == "UpToDate"

        trained_status = ["UpToDate", "Success"]
        while not is_trained:
            time.sleep(1)
            status = self.auth_client.train.get_status(
                self.app_id, self.app_version
            )
            is_trained = all(m.details.status in trained_status for m in status)
        print("App is trained.")

    def parse_file(self, data):
        utterances = []

        print("LOADING...", len(data))
        bar1 = tqdm(
            total=len(data),
            position=0,
            dynamic_ncols=True,
            leave=True,
            unit="file",
            desc="Parsing turns",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
        )
        for i, user in enumerate(data):
            # ic("turn")
            if "user_id" not in user:
                return "Users must have id"
            turn = user["turns"][0]
            if "db" in turn:
                continue
            item = turn['labels']['acts']
            if len(item) > 0:
                potential_intent = item[0]['args']
                if len(potential_intent) > 0 and potential_intent[0]['key'] == 'intent':
                    res = self.check_entities_and_build_utterances(item, turn['text'])
                    if res is not None:
                        utterances = utterances + res
            bar1.update(int(1))
        return utterances

    def send_batches(self, utterances):
        index = 0
        bar1 = tqdm(
            total=((len(utterances) + 1) - 100) // 100,
            position=0,
            dynamic_ncols=True,
            leave=True,
            unit="file",
            desc="Sending batches",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
        )

        while index < len(utterances) - 100:
            client.examples.batch(
                self.app_id,
                self.app_version,
                utterances[index: index + 100],
            )
            index += 100
            bar1.update(int(1))

        client.examples.batch(
            self.app_id,
            self.app_version,
            utterances[index: len(utterances)],
        )

    def build_other_utterances(self):
        cancel_examples = CONFIG.CANCEL_EXAMPLES
        none_examples = CONFIG.NONE_EXAMPLES
        # ic(none_examples)
        utterances_list = []

        bar1 = tqdm(
            total=len(cancel_examples) + len(none_examples),
            position=0,
            dynamic_ncols=True,
            leave=True,
            unit="file",
            desc="Building other entities",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
        )
        for item in cancel_examples:
            utterance = dict()
            utterance["intentName"] = "Cancel"
            utterance["text"] = item
            utterances_list.append(utterance)
            bar1.update(int(1))
        for item in none_examples:
            utterance = dict()
            utterance["intentName"] = "None"
            utterance["text"] = item
            utterances_list.append(utterance)
            bar1.update(int(1))
        return utterances_list

    def get_example_label(self, utterance, entity_name, value):
        """Build a EntityLabelObject.
        This will find the "value" start/end index in "utterance", and assign it to "entity name"
        """
        utterance = utterance.lower()
        value = value.lower()
        return {
            "entityName": entity_name,
            "startCharIndex": utterance.find(value),
            "endCharIndex": utterance.find(value) + len(value),
        }

    def check_entities_and_build_utterances(self, args, text):
        entities = []
        utterances = []
        if len(args) == 0:
            return
        utterance = dict()
        for arg in args[1:]:
            for ent in arg['args']:
                # ic(ent)
                if "val" not in ent:
                    continue
                entity = None

                if ent["key"] in entities_dict:
                    entity = entities_dict[ent["key"]]
                    entity = self.get_example_label(text, entity, ent["val"])
                    entities.append(entity)
        utterance["intentName"] = "BookFlight"
        utterance["entityLabels"] = entities
        utterance["text"] = text
        if len(utterance) > 0:
            utterances.append(utterance)
        return utterances

    def save_test_file(self):
        formatted_data = []
        for item in self.test_sample:
            item["intent"] = item.pop("intentName")
            item["entities"] = []
            if "entityLabels" in item:
                item.pop("entityLabels")
            formatted_data.append(item)
            # id(formatted_data)
        with open("test.json", "w") as outfile:
            json.dump(formatted_data, outfile)

    def predict(self):
        item = random.randint(0, len(self.test_sample))
        req = self.test_sample[item]['text']
        response = pred_client.prediction.resolve(
            CONFIG.LUIS_APP_ID, query=req
        )

        text = response.query
        top_intent = response.top_scoring_intent.intent
        all_entities = response.entities

        print('Utterance: ', text)
        print('Top Intent: ', top_intent)
        for i in range(0, len(all_entities)):
            print(all_entities[i].type, ' : ', all_entities[i].entity)
