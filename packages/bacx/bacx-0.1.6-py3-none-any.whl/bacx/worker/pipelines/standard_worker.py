import importlib
import logging
import os
import signal
import sys
import tempfile
from functools import wraps
from types import ModuleType
from typing import Any, Optional, TypeVar, Union

from bacx.storage.engines.engine import StorageEngine
from bacx.storage.manager import StorageManager
from bacx.utils.import_utils import import_from_module
from bacx.worker.base_worker import BaseWorker
from bacx.worker.types import JobDescription, JobResult


def _prepare_input_files(job: JobDescription, workdir: str, storage_data: StorageEngine):
    input_files = job.input_files or []
    local_files = [os.path.join(workdir, os.path.basename(file)) for file in input_files]
    for remote_file, local_file in zip(input_files, local_files):
        storage_data.download_to_file(remote_file, local_file)
    return job.set_input_files(local_files)


def _save_output_files(job: JobDescription, result: JobResult, workdir: str, storage_data: StorageEngine):
    remote_files = [
        os.path.join(job.input_data["storage_path"], file[len(workdir) :].lstrip("/"))
        for file in result.output_files
        if file.startswith(workdir)
    ]
    for remote_file, local_file in zip(remote_files, result.output_files):
        storage_data.upload_from_file(remote_file, local_file)

    # TODO reimplement transform_urls
    return JobResult(output_data=result.output_data, output_files=remote_files, error=result.error)


def wrap_predict(predictor_module, storage_data: StorageEngine, debug: bool):
    predict_fn = predictor_module.predict

    @wraps(predict_fn)
    def wrapper(models: dict, job: JobDescription) -> Optional[JobResult]:
        if debug:
            # in debug mode, we want to refresh implementation without need of restarting worker
            importlib.reload(predictor_module)
            fn = predictor_module.predict
        else:
            fn = predict_fn

        with tempfile.TemporaryDirectory() as workdir:
            job_local = _prepare_input_files(job, workdir, storage_data)
            result_local = fn(models, workdir, job_local)
            return _save_output_files(job, result_local, workdir, storage_data)

    return wrapper


T = TypeVar("T")


def load_with_environ(value: T, loader: callable, env_name: str, env_default: T = None) -> T:
    if value is None:
        value = os.environ.get(env_name, env_default)
    if value is None or value == "":
        raise EnvironmentError(f"Missing {env_name} in the environment.")
    if isinstance(value, str):
        return loader(value)

    return value


def _signal_handler(sig, frame):
    logging.info(f"Terminating... received signal {sig}")
    # TODO check all running predicts and drop jobs
    sys.exit(0)


def run_standard_worker(
    predictor_module: Union[str, ModuleType] = None,
    worker_class: Union[str, type(BaseWorker)] = None,
    storage_manager: Union[str, StorageManager] = None,
    *,
    init_signals: bool = True,
    init_logger: bool = True,
    debug: bool = None,
):
    if init_signals:
        signal.signal(signal.SIGINT, _signal_handler)
        signal.signal(signal.SIGTERM, _signal_handler)
    if init_logger:
        logging.basicConfig(level=logging.INFO)

    predictor_module: Any = load_with_environ(predictor_module, importlib.import_module, "PREDICTOR")
    worker_class: type(BaseWorker) = load_with_environ(worker_class, import_from_module, "WORKER_CLASS")
    storage_manager = load_with_environ(storage_manager, StorageManager, "STORAGE_CONFIG")
    storage_data = storage_manager["storage_data"]
    debug = bool(load_with_environ(debug, int, "DEBUG", False))

    worker = worker_class(
        job_type=predictor_module.JOB_TYPE,
        predict_fn=wrap_predict(predictor_module, storage_data, debug),
        load_fn=predictor_module.load_models,
    )
    worker.run()


if __name__ == "__main__":
    run_standard_worker()
