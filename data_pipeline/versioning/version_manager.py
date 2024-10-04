import mlflow
from mlflow.tracking import MlflowClient

class VersionManager:
    def __init__(self, experiment_name):
        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()

    def log_model(self, model, model_name, params=None, metrics=None):
        with mlflow.start_run():
            if params:
                mlflow.log_params(params)
            if metrics:
                mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, model_name)

    def load_model(self, model_name, version=None):
        if version:
            model_uri = f"models:/{model_name}/{version}"
        else:
            model_uri = f"models:/{model_name}/latest"
        return mlflow.sklearn.load_model(model_uri)

    def log_data(self, data, data_name):
        with mlflow.start_run():
            mlflow.log_artifact(data, data_name)

    def load_data(self, data_name, version=None):
        if version:
            run_id = self.client.get_run(version).info.run_id
        else:
            run_id = self.client.search_runs(experiment_ids=[mlflow.get_experiment_by_name(self.experiment_name).experiment_id])[0].info.run_id
        return mlflow.artifacts.load_artifact(run_id, data_name)

# Uso:
# version_manager = VersionManager("my_experiment")
# version_manager.log_model(my_model, "text_classifier", params={"max_depth": 5}, metrics={"accuracy": 0.95})
# loaded_model = version_manager.load_model("text_classifier", version=1)
# version_manager.log_data("path/to/data.csv", "training_data")
# loaded_data = version_manager.load_data("training_data")