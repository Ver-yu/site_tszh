# forum/utils.py
BAD_WORDS = [
    'мат1', 'мат2', 'мат3'  # Замените на реальный список нецензурных слов
]

def check_profanity(text):
    """Проверка текста на наличие нецензурных слов"""
    text_lower = text.lower()
    for word in BAD_WORDS:
        if word in text_lower:
            return True
    return False