import argparse
from split_message import split_message, MessageSplitError, MAX_LEN


def main():
    parser = argparse.ArgumentParser(description="Разделение HTML-сообщения на фрагменты.")
    parser.add_argument("file", type=str, help="Путь к файлу с исходным HTML.")
    parser.add_argument(
        "--max-len", type=int, default=MAX_LEN, help="Максимальная длина одного фрагмента."
    )
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as file:
        source = file.read()

    try:
        for idx, fragment in enumerate(split_message(source, args.max_len), start=1):
            print(f"Fragment #{idx}: {len(fragment)} chars")
            print(fragment)
            print("-" * 80)
    except MessageSplitError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    print('main works')
    main()
