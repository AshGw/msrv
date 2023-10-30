import random
import time
from datetime import datetime

from app.lib.hf.consts import ReadAccessTokens
from app.lib.hf.main import HF
from app.lib.hf.parser import StringAttributeParser, get_key_by_value
from app.lib.hf.switcher import get_valid_token, set_limited_key
from app.lib.logger.main import logging_service


class HFServiceCoordinator:
    generated_text: str = None
    generated_image: bytes

    def __init__(
        self,
        *,
        starter_hg_token: str,
        diffusion_model: str,
        prompt_model: str,
        prompt: str,
        use_prompt_enhancers: bool = False,
    ):
        self.tokens_dict: dict = StringAttributeParser(ReadAccessTokens).turn_dict()
        self.current_token = starter_hg_token
        self.diffusion_model = diffusion_model
        self.prompt_model = prompt_model
        self.prompt = prompt
        self.use_prompt_enhancers = use_prompt_enhancers

    def set_current_token(self, valid_hg_token: str):
        self.current_token = valid_hg_token

    @staticmethod
    def parse_prompts(prompt: str):
        return "".join(
            [char.upper() if random.random() < 0.5 else char.lower() for char in prompt]
        )

    def post_initializer(self):
        ...

    #   TODO:  ACTUALLY PARSE THE PROMPTS

    def run_prompter(self):
        while True:
            logging_service(f"PROMPT:{self.prompt}")
            # TODO: PLUG THIS INTO ANOTHER LOGGING SERVICE FOR LATER DATA PROCESSING
            prompt_result = HF(
                api_key=self.current_token, model=self.prompt_model
            ).send(prompt=self.parse_prompts(self.prompt))
            prompt_attributes = prompt_result.get_attrs()

            if prompt_attributes.get("reached_rate_limit"):

                logging_service(
                    "Rate limit reached, updated token.", datetime.now().isoformat()
                )

                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key)
                self.set_current_token(get_valid_token())

                continue

            if prompt_attributes.get("is_token_invalid"):

                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key)
                self.set_current_token(get_valid_token())

                logging_service(
                    "Invalid token, updated token.", datetime.now().isoformat()
                )
                continue  # Continue the loop to retry with the new token

            if prompt_attributes.get("is_overloaded"):

                logging_service(
                    "Server overloaded, retrying with a new token.",
                    datetime.now().isoformat(),
                )

                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key)
                self.set_current_token(get_valid_token())

                continue

            if prompt_attributes.get("is_error_unknown"):

                logging_service(
                    "Unknown error, asking client to try again.",
                    datetime.now().isoformat(),
                )
                # bounce an error message to the client

                continue

            if prompt_attributes.get("is_unseen_error"):
                logging_service(
                    "Unseen error, asking client to try again.",
                    datetime.now().isoformat(),
                )

                continue

            if prompt_attributes.get("estimated_time") > 0.0:
                ...
                logging_service(
                    f"Model is loading, estimated time: {prompt_attributes.get('estimated_time')}, asking client to try again.",
                    datetime.now().isoformat(),
                )
                # Inform the client about the delay
                continue

            break

        return prompt_result
        # Continue with the rest of flow logic

    def run_diffusion(self):
        prompt = (
            self.run_prompter().generated_text()
            if self.use_prompt_enhancers is True
            else self.parse_prompts(self.prompt)
        )
        while True:
            prompt_result = HF(
                api_key=self.current_token, model=self.diffusion_model
            ).send(prompt=prompt)
            prompt_attributes = prompt_result.get_attrs()

            if prompt_attributes.get("reached_rate_limit"):

                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key)
                self.set_current_token(get_valid_token())

                logging_service(
                    "Rate limit reached, updated token.", datetime.now().isoformat()
                )

                continue

            if prompt_attributes.get("is_token_invalid"):

                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key)
                self.set_current_token(get_valid_token())

                logging_service(
                    "Invalid token, updated token.", datetime.now().isoformat()
                )

                continue  # Continue the loop to retry with the new token

            if prompt_attributes.get("is_overloaded"):

                logging_service(
                    "Server overloaded, retrying with a new token.",
                    datetime.now().isoformat(),
                )

                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key)
                self.set_current_token(get_valid_token())

                continue

            if prompt_attributes.get("is_error_unknown"):
                logging_service(
                    "Unknown error, asking client to try again.",
                    datetime.now().isoformat(),
                )
                # bounce an error message to the client (not shown in code)
                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key, expiration=10)
                self.set_current_token(get_valid_token())

                continue

            if prompt_attributes.get("is_unseen_error"):
                logging_service(
                    "Unseen error, asking client to try again.",
                    datetime.now().isoformat(),
                )
                expired_key = get_key_by_value(
                    d=self.tokens_dict, target_value=self.current_token
                )
                set_limited_key(key=expired_key, expiration=10)
                self.set_current_token(get_valid_token())

                continue

            if prompt_attributes.get("estimated_time") > 0.0:
                ...
                logging_service(
                    f"Model is loading, estimated time: {prompt_attributes.get('estimated_time')}, asking client to try again.",
                    datetime.now().isoformat(),
                )
                # Inform the client about the delay
                continue

            break

        return prompt_result
        # Continue with the rest of flow logic

    def get_generated_text(self):
        return self.run_prompter().generated_text()

    def get_raw_image(self):
        return self.run_diffusion().generated_raw_image()
