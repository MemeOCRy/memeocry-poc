import json
from os import listdir
from os.path import isfile, join

import easyocr
from rapidfuzz import fuzz, process, utils

memeocry_path = "memeocry.json"


def extract_text_for_lang(image_paths: list[str], lang: str) -> list[dict[str, str]]:
    reader = easyocr.Reader([lang])
    return [
        {
            "path": image_path,
            "text": " ".join(reader.readtext(image_path, detail=0)),  # type: ignore
            "lang": lang,
        }
        for image_path in image_paths
    ]


def extract_text(image_paths: list[str], langs: list[str]) -> list[dict[str, str]]:
    return [text for lang in langs for text in extract_text_for_lang(image_paths, lang)]


def update(folder: str, langs: list[str]) -> int:
    images = [
        join(folder, image) for image in listdir(folder) if isfile(join(folder, image))
    ]
    texts = extract_text(images, langs)
    with open(memeocry_path, mode="w", encoding="utf-8") as file:
        json.dump(texts, file, ensure_ascii=False, indent=4, sort_keys=True)
    return len(images)


def search(query: str):
    with open(memeocry_path, mode="r", encoding="utf-8") as read_file:
        memeocry_json = json.load(read_file)

    texts = [entry["text"] for entry in memeocry_json]
    results = process.extract(
        query,
        texts,
        scorer=fuzz.token_set_ratio,
        limit=5,
        processor=utils.default_process,
    )

    return [memeocry_json[index] for _, _, index in results]
