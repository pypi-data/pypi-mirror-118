import time
from threading import Thread

from .mysql_accessor import MysqlAccessor
from .algorithm_manager import alg_manager
from .dispatcher import dispatcher
from .logger import log


class Checker(Thread):
    update_time_mapping = {}
    running = False

    def run(self):
        if self.running:
            return

        self.running = True

        while True:
            try:
                algs = alg_manager.alg_mapping.keys()
                for algorithm in algs:
                    update_time = MysqlAccessor.check_load_update_time(algorithm)
                    if not update_time:
                        continue

                    if (
                        algorithm not in self.update_time_mapping
                        or update_time > self.update_time_mapping[algorithm]
                    ):
                        log.info(f"checking {algorithm}, has update")
                        models = MysqlAccessor.get_load_models(algorithm)
                        to_load_models = models.keys()
                        loaded_models = dispatcher.get_loaded_models()
                        need_load_models = to_load_models - loaded_models
                        need_unload_models = loaded_models - to_load_models

                        log.info(f"loading {algorithm} models, {need_load_models}")
                        for model_id in need_load_models:
                            dispatcher.dispatch_load(
                                algorithm, model_id, models[model_id]
                            )

                        log.info(f"unloading {algorithm} models, {need_unload_models}")
                        for model_id in need_unload_models:
                            dispatcher.dispatch_unload(algorithm, model_id)

                        self.update_time_mapping[algorithm] = update_time
                    else:
                        log.info(f"checking {algorithm}, nothing to update")
            except Exception as ex:
                log.error("check fail", ex)

            time.sleep(5)


checker = Checker()
