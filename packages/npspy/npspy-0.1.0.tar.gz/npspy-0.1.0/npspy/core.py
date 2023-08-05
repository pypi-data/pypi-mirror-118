from typing import Dict, Iterable, Literal

Categories = Literal["detractor", "passive", "promoter"]


class InvalidAnswerError(Exception):
    """Class for invalid answer related errors."""

    pass


def categorize(answer: int) -> Categories:
    """Categorize an answwer for the NPS question.
    Args:
        answer: An answer for the NPS question.
    Returns:
        Answerer's category.
    Raises:
        InvalidAnswerError: If the answer is not between 0 and 10.
    """
    if 0 <= answer <= 6:
        return "detractor"
    elif 7 <= answer <= 8:
        return "passive"
    elif 9 <= answer <= 10:
        return "promoter"
    else:
        raise InvalidAnswerError(f"Invalid answer: {answer}")


def calculate(answers: Iterable[int]) -> float:
    """Calculates nps.
    Args:
        answers: Answers for the NPS question.
    Returns:
        Calculated nps.
    """
    count: Dict[Categories, int] = {}
    for answer in answers:
        category = categorize(answer)
        count[category] = count.get(category, 0) + 1
    nps = (
        (count.get("promoter", 0) - count.get("detractor", 0))
        / sum(count.values())
        * 100
    )
    return nps
