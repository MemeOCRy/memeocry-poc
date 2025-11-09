import json
from os import listdir
from os.path import isfile, join

import easyocr
from rapidfuzz import fuzz, process, utils


def extract_text(image_paths: list[str], lang: str) -> list[dict]:
    reader = easyocr.Reader([lang])
    return [
        {"path": image_path, "text": " ".join(reader.readtext(image_path, detail=0))}  # type: ignore
        for image_path in image_paths
    ]


def get_image_paths(folder: str):
    return [
        join(folder, image) for image in listdir(folder) if isfile(join(folder, image))
    ]


def extract_texts_to_list(image_paths: list[str], lang: str) -> list[str]:
    reader = easyocr.Reader([lang])
    return [
        " ".join(reader.readtext(image_path, detail=0))  # type: ignore
        for image_path in image_paths
    ]


def update(folder: str, langs: list[str]):
    images = [
        join(folder, image) for image in listdir(folder) if isfile(join(folder, image))
    ]
    texts = [text for lang in langs for text in extract_text(images, lang)]
    with open("memeocry.json", mode="w", encoding="utf-8") as file:
        json.dump(texts, file, ensure_ascii=False, indent=4, sort_keys=True)
    return


def search(text: str) -> list[dict]:
    return [{"path": "", "text": ""}]


def main():
    texts = extract_texts_to_list(get_image_paths("images"), "de")
    # print(fuzz.token_set_ratio("ostfront", text, processor=utils.default_process))
    print(
        process.extract(
            "normie",
            texts,
            scorer=fuzz.token_set_ratio,
            limit=10,
            processor=utils.default_process,
        )
    )


if __name__ == "__main__":
    main()
