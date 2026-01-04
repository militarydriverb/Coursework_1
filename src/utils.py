import json
import logging

logging.basicConfig(
    filename="logs/utils.log",
    encoding="utf-8",
    filemode="w+",
    format="%(asctime)s %(filename)s %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger(__name__)


def dic_list(path: str) -> list[dict]:
    """
    Загружает финансовые транзакции из JSON-файла.

    Принимает путь до JSON-файла и возвращает список словарей
    с данными о финансовых транзакциях.

    Args:
        path: Путь к JSON-файлу

    Returns:
        list[dict]: Список словарей с транзакциями или пустой список при ошибке

    Example:
        >>> dic_list("data/operations.json")
        [{"id": 1, "amount": 100, ...}, ...]
    """
    try:
        logger.info("function dis_list is started")
        with open(path, "r", encoding="utf-8") as f:
            logger.info("file is found and open")
            try:
                transactions = json.load(f)
                if isinstance(transactions, list):
                    logger.info("file is the list, return transaction success")
                    return transactions
                else:
                    logger.error("file is not the list Incorrectness")
                    return []
            except json.JSONDecodeError:
                logger.error("JSONDecodeError")
                return []
    except FileNotFoundError:
        logger.error("file is not found please check the path")
        return []


if __name__ == "__main__":
    path = "data/operations.json"  # pragma: no cover
    print(dic_list(path))  # pragma: no cover
