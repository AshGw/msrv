import unittest

from app.lib.exceptions import EmptyPromptError
from app.lib.hf.consts import Models, PersonalKeys
from app.lib.hf.main import HF


class HFTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.api_key = PersonalKeys.MY_API_KEY
        self.prompt_model = Models.PROMPT

    def test_empty_prompt(self):
        with self.assertRaises(EmptyPromptError):
            self.result = HF(api_key=self.api_key, model=self.prompt_model).send(
                prompt=""
            )
