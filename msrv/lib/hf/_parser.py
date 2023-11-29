import random
from typing import Any, Dict, Generator, Tuple
from msrv.lib.env import Env, EnvStringAttributes

from msrv.lib.hf._interfaces import NextToken
from msrv.lib.hf.consts import HFGetDiffuserAttrs
from msrv.lib.exceptions import EmptyPromptError

_TOKEN_CLS = Env.Prod.HF.KEYS.ExecTokens

# TODO: TEST THIS MODULE


class StringAttributeParser:
    def __init__(self, cls: EnvStringAttributes):
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

    def next(self) -> Tuple[str, str]:
        return next(self.generator)


def get_next_token(
    *, generator: Generator[Tuple[str, str], bool, None], flag: bool
) -> NextToken:
    """
    Retrieves the stored HF access tokens where each token is valid
    and not currently loaded nor rate limited
    """
    key, value = generator.send(flag)
    return NextToken(token_identifier=key, token=value, is_new=flag)


def initialize_generator() -> Generator[tuple[str, str], bool, None]:
    """Returns the generator object to be passed later"""
    return StringAttributeParser(_TOKEN_CLS).generator


def get_key_by_value(d: dict, target_value: Any) -> str | None:
    """
    Get the key associated with a specific value in the dictionary.
    Returns None if the value is not found.
    """
    for key, value in d.items():
        if value == target_value:
            return key
    return None


def get_random_token() -> str:
    tokens_dict = StringAttributeParser(_TOKEN_CLS).turn_dict()
    return random.choice(list(tokens_dict.values()))


def parse_prompt(prompt: str) -> str:
    length = len(prompt)
    if (
        length < HFGetDiffuserAttrs.HF_MIN_PROMPT_SIZE
        or length > HFGetDiffuserAttrs.HF_MAX_PROMPT_SIZE
    ):
        raise EmptyPromptError()
    return "".join(
        [
            char.upper() if random.random() < 0.5 else char.lower()
            for char in prompt.lower()
        ]
    )


if __name__ == "__main__":
    a = get_random_token()
    print(a)
