import traceback
from collections import defaultdict
from threading import Lock

import random

from .algorithm_manager import alg_manager
from .api_util import catch_exception
from .config import client_config
from .logger import log
from .service_response import (
    success_response,
    success_response_with_data,
    format_service_response,
    error_response,
)
from .validation.exceptions import ArgValueError, Warn
from .worker import Worker
if client_config.connect_kafka:
    from .kafka_accessor import predict_tracker


class Dispatcher:
    def __init__(self):
        self.num_worker = client_config.num_worker
        self.num_thread = client_config.num_thread
        self.model_load_mapping = defaultdict(list)
        self.status_lock = Lock()
        self.workers = []
        for _ in range(self.num_worker):
            worker = Worker()
            self.workers.append(worker)

    def get_loaded_models(self):
        return [k for k in self.model_load_mapping if len(self.model_load_mapping[k])]

    def get_info(self):
        info = {
            "load": self.model_load_mapping,
            "algorithms": list(alg_manager.alg_mapping.keys()),
        }
        return format_service_response(success_response_with_data(info))

    def register(self, name, alg):
        alg_manager.register(name, alg)
        for worker in self.workers:
            worker.work("init_alg", alg_manager.alg_mapping)

    def unregister(self, name):
        alg_manager.unregister(name)
        for worker in self.workers:
            worker.work("remove_alg", name)

    @catch_exception
    def dispatch_predict(self, model_id, features, uuid, params):
        if (
            model_id not in self.model_load_mapping
            or len(self.model_load_mapping[model_id]) == 0
        ):
            log.warn("model [{}] not loaded".format(model_id))
            if client_config.connect_kafka:
                predict_tracker.send(
                    message="predict model not loaded",
                    reason="model [{}] not loaded".format(model_id),
                )
            raise Warn(message="model [{}] not loaded".format(model_id))

        candidates = self.model_load_mapping[model_id]
        index = random.choice(candidates)
        worker = self.workers[index]
        try:
            success, predictions = worker.work(
                "predict",
                {
                    "model_id": model_id,
                    "features": features,
                    "uuid": uuid,
                    "params": params,
                },
            )

            # 如果返回的是模型未加载，重置模型加载状态
            if not success and "load" in predictions:
                with self.status_lock:
                    self.model_load_mapping[model_id].remove(index)

        except Exception as e:
            log.error(e)
            traceback.print_exc()
            log.error("fail to call worker")
            if client_config.connect_kafka:
                predict_tracker.send(message="fail to call worker", reason=e)
            return format_service_response(error_response(message="worker fail"))

        if success:
            return format_service_response(
                success_response_with_data({"predictions": predictions})
            )
        else:
            return format_service_response(error_response(message=str(predictions)))

    @catch_exception
    def dispatch_unload(self, algorithm, model_id):
        if algorithm not in alg_manager.alg_mapping:
            raise ArgValueError(message="algorithm [{}] not support".format(algorithm))

        if model_id not in self.model_load_mapping:
            return format_service_response(success_response("model is not loaded"))

        with self.status_lock:
            for index in self.model_load_mapping[model_id]:
                self.workers[index].work(
                    "unload", {"algorithm": algorithm, "model_id": model_id}
                )

            self.model_load_mapping[model_id] = []
        return format_service_response(success_response())

    @catch_exception
    def dispatch_load(self, algorithm, model_id, model_path):
        if algorithm not in alg_manager.alg_mapping:
            raise ArgValueError(message="algorithm [{}] not support".format(algorithm))

        if (
            model_id in self.model_load_mapping
            and len(self.model_load_mapping[model_id]) > 0
        ):
            log.info("model is already loaded {}".format(model_id))
            if client_config.connect_kafka:
                predict_tracker.send(
                    message="model is already loaded",
                    reason="model is already loaded {}".format(model_id),
                )
            return format_service_response(success_response("model is already loaded"))
            # raise ArgValueError(message='model [{}] already loaded'.format(model_id))

        index = random.randint(0, self.num_worker - 1)
        worker = self.workers[index]
        success, message = worker.work(
            "load",
            {"model_id": model_id, "model_path": model_path, "algorithm": algorithm},
        )
        if success:
            with self.status_lock:
                self.model_load_mapping[model_id].append(index)
            return format_service_response(success_response())
        else:
            if client_config.connect_kafka:
                predict_tracker.send(message="load fail", reason=message)
            return format_service_response(error_response(message=message))


dispatcher = Dispatcher()


def register(name, alg):
    global dispatcher
    dispatcher.register(name, alg())


def unregister(name):
    global dispatcher
    dispatcher.unregister(name)
