from typing import Generator
from bs4 import BeautifulSoup

MAX_LEN = 4096


class MessageSplitError(Exception):
    """Исключение для ошибок разделения HTML."""
    ...


def split_message(source: str, max_len=MAX_LEN) -> Generator[str, None, None]:
    """
    Разделяет HTML-сообщение на фрагменты заданной длины с сохранением структуры тегов.
    :param source: Исходный HTML-текст.
    :param max_len: Максимальная длина одного фрагмента.
    :return: Генератор фрагментов.
    """
    soup = BeautifulSoup(source, "html.parser")
    current_fragment = ""
    current_length = 0
    open_tags = []

    for element in soup.contents:
        element_html = str(element)
        element_length = len(element_html)

        if element_length > max_len:
            raise MessageSplitError(
                f"Элемент слишком длинный ({element_length} символов) для одного фрагмента."
            )

        if current_length + element_length > max_len:
            current_fragment += "".join(f"</{tag.name}>" for tag in reversed(open_tags))
            yield current_fragment

            current_fragment = "".join(str(tag) for tag in open_tags)
            current_length = len(current_fragment)

        current_fragment += element_html
        current_length += element_length

        if element.name and not element.is_empty_element:
            open_tags.append(element)
        elif element.name and element in open_tags:
            open_tags.remove(element)

    if current_fragment:
        current_fragment += "".join(f"</{tag.name}>" for tag in reversed(open_tags))
        yield current_fragment
