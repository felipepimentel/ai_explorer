from flask import Flask, jsonify, request

from ..core import analysis_service, embedding_service, processing_service

app = Flask(__name__)


@app.route("/process", methods=["POST"])
def api_process_file():
    file_path = request.json["file_path"]
    processing_service.process_file(file_path)
    return jsonify({"status": "success"})


@app.route("/search", methods=["GET"])
def api_search():
    query = request.args.get("query")
    results = analysis_service.search(query, embedding_service)
    return jsonify(results)


@app.route("/clusters", methods=["GET"])
def api_clusters():
    cluster_info = analysis_service.get_cluster_info()
    return jsonify(cluster_info)


def start_api():
    app.run(debug=True)
