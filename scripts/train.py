import json
import random
import time

import bios
from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials
from sklearn.metrics import accuracy_score
from tqdm.auto import tqdm

config = bios.read("./train_config.yaml")
client = LUISAuthoringClient(
    config["authoringEndpoint"],
    CognitiveServicesCredentials(config["authoringKey"]),
)
TEST_SIZE = 0.05

entities_dict = {
    "dst_city": "To",
    "or_city": "From",
    "str_date": "dateTimeV2",
    "end_date": "dateTimeV2",
    "budget": "Budget",
}

intent_dict = {"book": "BookFlight"}


def get_example_label(utterance, entity_name, value):
    """Build a EntityLabelObject.
    This will find the "value" start/end index in "utterance", and assign it to "entity name"
    """
    # ic(entity_name)
    utterance = utterance.lower()
    value = value.lower()
    return {
        "entityName": entity_name,
        "startCharIndex": utterance.find(value),
        "endCharIndex": utterance.find(value) + len(value),
    }


def check_entities_and_build_utterances(args, turn):
    entities = []
    utterances = []
    if len(args) == 0:
        return
    for arg in args:
        if "val" not in arg.keys():
            break
        entity = None
        utterance = dict()
        if arg["key"] in entities_dict:
            # ic(arg)
            entity = entities_dict[arg["key"]]
        if entity is not None:
            # ic("NOT NONE")
            entity = get_example_label(turn["text"], entity, arg["val"])
            utterance["intentName"] = "BookFlight"
            entities.append(entity)
        else:

            utterance["intentName"] = "None"
        utterance["entityLabels"] = entities
        utterance["text"] = turn["text"]
        utterances.append(utterance)
    return utterances


def parse_file(data):
    utterances = []
    got_intent = False

    print("LOADING...", len(data))
    bar1 = tqdm(
        total=(len(utterances) - 100) // 100,
        position=0,
        dynamic_ncols=True,
        leave=True,
        unit="file",
        desc="Sending batches",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
    )
    for i, user in enumerate(data):
        if "user_id" not in user:
            return "Users must have id"
        turn = user["turns"][0]
        if "db" in turn:
            continue
        labels = turn["labels"]
        acts = labels["acts"]
        for act in acts:
            args = act["args"]
            for arg in args:
                if arg["key"] == "intent":
                    got_intent = True
                    continue
        if got_intent:
            res = check_entities_and_build_utterances(act["args"], turn)
            if res is not None:
                utterances = utterances + res
        bar1.update(int(1))
    return utterances


def train_app():
    # Training the model
    print("\nApp in training")

    async_training = client.train.train_version(
        config["app_id"], config["version_id"]
    )
    is_trained = async_training.status == "UpToDate"

    trained_status = ["UpToDate", "Success"]
    while not is_trained:
        time.sleep(1)
        status = client.train.get_status(
            config["app_id"], config["version_id"]
        )
        is_trained = all(m.details.status in trained_status for m in status)

    print("App is trained.")


def format_test_file(data):
    formatted_data = []
    for item in data:
        item["intent"] = item.pop("intentName")
        item["entities"] = []
        item.pop("entityLabels")
        formatted_data.append(item)
        id(formatted_data)
    with open("test.json", "w") as outfile:
        json.dump(formatted_data, outfile)


def send_batches(utterances):
    index = 0
    bar1 = tqdm(
        total=(len(utterances) - 100) // 100,
        position=0,
        dynamic_ncols=True,
        leave=True,
        unit="file",
        desc="Sending batches",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
    )

    while index < len(utterances) - 100:
        client.examples.batch(
            config["app_id"],
            config["version_id"],
            utterances[index: index + 100],
        )
        index += 100
        bar1.update(int(1))
    print("Sending last batch")
    client.examples.batch(
        config["app_id"],
        config["version_id"],
        utterances[index: len(utterances)],
    )


def main():
    filename = "../frames.json"
    with open(filename) as frames_file:
        data = json.load(frames_file)
    utterances = parse_file(data)
    print(len(utterances))
    send_batches(utterances)
    with open("../utterances.json", "w") as outfile:
        json.dump(utterances, outfile)
    sample_size = round(len(utterances) * TEST_SIZE)
    random.shuffle(utterances)
    test_sample = utterances[:sample_size]
    utterances = utterances[sample_size:]

    train_app()
    with open("../test.json") as frames_file:
        test_sample = json.load(frames_file)

    client = LUISRuntimeClient(
        config["predictionEndpoint"],
        CognitiveServicesCredentials(config["predictionKey"]),
    )
    y_true = []
    y_pred = []
    bar1 = tqdm(
        total=(len(utterances) - 100) // 100,
        position=0,
        dynamic_ncols=True,
        leave=True,
        unit="file",
        desc="Sending batches",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]",
    )
    for item in test_sample:
        y_true.append(item["intent"])
        try:
            result = client.prediction.resolve(config["app_id,"], item["text"])
            y_pred.append(result.top_scoring_intent.intent)
            # ic(item["intent"], result.top_scoring_intent.intent)
        except Exception as err:
            print("Encountered exception. {}".format(err))
        bar1.update(int(1))
    print("Model accuracy: {}".format(accuracy_score(y_true, y_pred)))


if __name__ == "__main__":
    random.seed(42)
    client = LUISAuthoringClient(
        config["authoringEndpoint"],
        CognitiveServicesCredentials(config["authoringKey"]),
    )
    main()
