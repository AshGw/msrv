from typing import Any, Dict, Generator, Tuple

from app.lib.hf.consts import ReadAccessTokens, StringAttributes


class StringAttributeParser:
    def __init__(self, cls: StringAttributes):
        self.cls = cls
        self.generator: Generator[Tuple[str, str], bool, None] = self.dict_generator(
            self.turn_dict()
        )
        self.next()

    @staticmethod
    def dict_generator(dict: Dict[str, str]) -> Generator[Tuple[str, str], bool, None]:
        """
        Runs through every dictionary key & value pair in a closed loop
        """
        items = list(dict.items())
        i = 0

        while True:
            if i >= len(items):
                i = 0

            key, value = items[i]
            go_next = yield key, value

            if go_next:
                i += 1

    def turn_dict(self) -> Dict[str, str]:
        """
        Turns any class string attrs into a dictionary
        """
        messy_dict = vars(self.cls)
        attrs_dict = {
            k: v
            for k, v in messy_dict.items()
            if isinstance(v, str) and not k.startswith("__")
        }
        return attrs_dict

    def next(self):
        return next(self.generator)


def get_next_token(
    *, generator: Generator[tuple[str, str], bool, None], flag: bool
) -> Dict[str, str]:
    """
    Retrieves the stored HF access tokens where each token is valid
    and not currently loaded nor rate limited
    """
    key, value = generator.send(flag)
    return {"token_identifier": key, "token": value, "is_new": flag}


def initialize_generator() -> Generator[tuple[str, str], bool, None]:
    """Returns the generator object to be passed later"""
    return StringAttributeParser(ReadAccessTokens).generator


def get_key_by_value(d: dict, target_value: Any):
    """
    Get the key associated with a specific value in the dictionary.
    Returns None if the value is not found.
    """
    for key, value in d.items():
        if value == target_value:
            return key
    return None


if __name__ == "__main__":
    myDict = StringAttributeParser(ReadAccessTokens).turn_dict()
    print(myDict)
    print()
