"""
Copyright (c) 2021 NLPHub AI Singapore

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import tarfile

import requests
from stanza.resources import common
from tqdm import tqdm

POS_MODELS = {
    "pos-id-ud-bilstm",
    "pos-id-ud-indobert",
    "pos-id-ud-xlmr",
    "pos-id-ud-xlmr-best",
    "pos-th-ud-bilstm",
    "pos-th-ud-bilstmcrf",
    "pos-th-ud-xlmr",
    "pos-th-ud-xlmr-best",
    "pos-vi-ud-bilstm",
    "pos-vi-ud-phobert",
    "pos-vi-ud-xlmr",
    "pos-vi-ud-xlmr-best",
}

NER_MODELS = {
    "ner-th-thainer-scratch",
    "ner-th-thainer-xlmr",
    "ner-th-thainer-xlmr-best",
    "ner-id-nergrit-xlmr",
    "ner-id-nergrit-xlmr-best",
}

CP_MODELS = {"cp-id-kethu-benepar-xlmr-best", "cp-id-kethu-xlmr"}

DP_MODELS = {
    "dp-id-ud-scratch",
    "dp-id-ud-indobert",
    "dp-id-ud-xlmr",
    "dp-id-ud-xlmr-best",
    "dp-th-ud-scratch",
    "dp-th-ud-xlmr",
    "dp-th-ud-xlmr-best",
    "dp-vi-ud-scratch",
    "dp-vi-ud-xlmr",
    "dp-vi-ud-xlmr-best",
}

AVAILABLE_MODELS = set().union(POS_MODELS, NER_MODELS, CP_MODELS, DP_MODELS)

CLOUD_STORAGE_URL = "https://seacorenlp.blob.core.windows.net/models/"

MODEL_TASK_FOLDER = {
    "pos": "tagging/pos/",
    "ner": "tagging/ner/",
    "cp": "parsing/constituency/",
    "dp": "parsing/dependency/",
}


def _check_if_model_is_valid(model_name: str) -> None:
    assert model_name in AVAILABLE_MODELS, (
        f"Model selected ({model_name}) is not available. "
        + "Please refer to our documentation to see which models are currently available."
    )


def _check_if_task_is_valid(model_task: str, class_task: str) -> None:
    assert (
        model_task == class_task
    ), "The model selected cannot be used with the class selected."


def _model_exists_in_local(model_name: str) -> bool:
    if not os.path.exists(f"{model_name}.tar.gz") and not os.path.exists(
        model_name
    ):
        return False
    else:
        return True


def download_model(model_name: str) -> None:
    """
    Downloads a model from cloud storage based on its name.
    Model names are structured {task}-{language}-{dataset}-{embedding}.
    """

    task = model_name.split("-")[0]
    model_zip_name = model_name + ".tar.gz"
    url = CLOUD_STORAGE_URL + MODEL_TASK_FOLDER[task] + model_zip_name

    r = requests.get(url, stream=True)
    with open(model_zip_name, "wb") as f:
        file_size = int(r.headers.get("content-length"))
        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            desc=f"Downloading {model_name}...",
        ) as progress:
            for chunk in r.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    progress.update(len(chunk))
            progress.close()

    # Benepar models have to be run as a folder, not gzip file
    if task == "cp" and "benepar" in model_name:
        with tarfile.open(model_zip_name) as zip_file:
            zip_file.extractall()
            zip_file.close()
            os.remove(model_zip_name)


def download_model_if_absent(model_name: str) -> None:
    if _model_exists_in_local(model_name):
        print(f"Loading {model_name} from local cache...")
    else:
        download_model(model_name)


def check_stanza_model_exists_in_local(
    lang: str, stanza_model_dir: str = common.DEFAULT_MODEL_DIR
) -> bool:
    """
    Raises exception if Stanza models are not found in the default folder
    and prompts user to download the model before proceeding. Returns True
    if the model folder has been found.
    """
    lang_model_path = os.path.join(stanza_model_dir, lang)
    if not (os.path.isdir(lang_model_path)):
        raise Exception(
            f"Stanza model for lang='{lang}' has not been downloaded, please do stanza.download('{lang}') before proceeding"
        )

    return True
