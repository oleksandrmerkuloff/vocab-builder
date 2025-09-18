from googletrans import Translator

import asyncio
from string import punctuation


async def translate_words(unique_words: set, all_words: list):
    async with Translator() as translator:
        tasks = [translator.translate(word, dest='ru', src='en') for word in unique_words]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        storage = []
        for word, res in zip(unique_words, results):
            if isinstance(res, Exception):
                storage.append(
                    [
                        word, f"[error: {type(res).__name__}]",
                        str(all_words.count(word))
                        ]
                    )
            else:
                storage.append([word, res.text, str(all_words.count(word))])
        return storage


def get_words(master, file, func):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            translator = str.maketrans('', '', punctuation)
            splitted_file = f.read().translate(translator).split()
            words = [w.lower() for w in splitted_file if not w.isdigit()]
            unique_words = set(words)
        storage = asyncio.run(translate_words(unique_words, words))
        master.after(0, lambda: func(master, storage))
    except FileExistsError:
        raise FileExistsError('File doesn\'t exists.\nTry Again!')
    except FileNotFoundError:
        raise FileNotFoundError('Wrong path for file.\nTry Again!')
