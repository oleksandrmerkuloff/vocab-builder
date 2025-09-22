from googletrans import Translator

from string import punctuation


translator = Translator()


# def translate_words(unique_words: set, all_words: list):
#     translator = Translator()
#     storage = []
#     for word in unique_words:
#         try:
#             res = translator.translate(word, dest='ru', src='en')
#             storage.append([word, res.text, str(all_words.count(word))])
#         except Exception as e:
#             storage.append([word, f"[error: {type(e).__name__}]", str(all_words.count(word))])
#     return storage


async def get_words(master, file, func):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            translator = str.maketrans('', '', punctuation)
            splitted_file = f.read().translate(translator).split()
            words = [w.lower() for w in splitted_file if not w.isdigit()]
            unique_words = set(words)

        total = len(unique_words)
        storage = []
        translator = Translator()

        for index, word in enumerate(unique_words, 1):
            try:
                result = await translator.translate(word, dest='ru', src='en')
                storage.append([word, result.text, str(words.count(word))])
            except Exception as e:
                storage.append([word, f"[error: {type(e).__name__}]", str(words.count(word))])

            progess = index / total
            master.after(0, lambda p=progess: master.progress_bar.set(p))
            master.after(0, lambda: master.progress_label.configure(text=f'{index}/{total}'))

        storage.sort(key=lambda x: int(x[2]), reverse=True)
        master.after(0, lambda: func(master, storage))
    except FileNotFoundError:
        raise FileNotFoundError('Wrong path for file.\nTry Again!')
