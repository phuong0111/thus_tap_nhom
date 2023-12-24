from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import logging
import logging.config
from pythonjsonlogger import jsonlogger
from datetime import datetime


class ElkJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(ElkJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record["@timestamp"] = datetime.now().isoformat()
        log_record["level"] = record.levelname
        log_record["logger"] = record.name


def enable_urllib3_logging():
    logging.config.fileConfig("to-do-app/logging.conf")
    logging.getLogger().setLevel(logging.DEBUG)


app = Flask(__name__)

client = MongoClient(
    host="test_mongodb",
    port=27017,
    username="root",
    password="pass",
    authSource="admin",
)
db = client.mytododb
tasks_collection = db.tasks


@app.route("/")
def index():
    tasks = tasks_collection.find()
    return render_template("index.html", tasks=tasks)


@app.route("/add_task", methods=["POST"])
def add_task():
    task_name = request.form.get("task_name")
    if task_name:
        tasks_collection.insert_one({"name": task_name})
    return redirect(url_for("index"))


@app.route("/delete_task/<task_id>", methods=["GET"])
def delete_task(task_id):
    tasks_collection.delete_one({"_id": ObjectId(task_id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    enable_urllib3_logging()
    app.run(host="0.0.0.0", debug=True)
