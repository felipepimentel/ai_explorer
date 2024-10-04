import mlflow
from mlflow.tracking import MlflowClient

class ModelVersioner:
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

# Exemplo de uso:
# versioner = ModelVersioner("my_experiment")
# versioner.log_model(my_model, "text_classifier", params={"max_depth": 5}, metrics={"accuracy": 0.95})
# loaded_model = versioner.load_model("text_classifier", version=1)