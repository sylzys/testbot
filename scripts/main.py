import argparse

from app_config import AppConfig
from app_create import LuisApp
from app_trainer import AppTrainer

CONFIG = AppConfig()

parser = argparse.ArgumentParser()

parser.add_argument("-f", "--file", action='store', metavar="path", type=str, help="Path to the json dataset (default frames.json)")
parser.add_argument("-t", "--train", action='store_true', help="Launch bot training")
parser.add_argument("-g", "--generate-test", action='store_true', help="Generate test file")
parser.add_argument("-p", "--predict", action='store_true', help="Predict score after training")

args = parser.parse_args()

if args.file is None:
    args.file = "./frames.json"

if __name__ == "__main__":
    print(args.file)
    print("--- Instanciating classes ---")
    app = LuisApp()

    print("--- Creating app ---")
    app_id, app_version = app.create_luis_app(name="FlyMeLuis2")

    print("--- Creating intents ---")
    app.create_luis_intents()

    print("--- Creating entities ---")
    app.create_luis_entities()

    print("--- Instanciating Trainer ---")
    trainer = AppTrainer(app_id, app_version)

    print("--- Training app ---")
    trainer.start_training(args.file)

    print("--- Saving test set as JSON ---")
    trainer.save_test_file()

    print("--- Publishing app ---")
    app.publish_app()

    print("--- Predicting ---")
    trainer.predict()
