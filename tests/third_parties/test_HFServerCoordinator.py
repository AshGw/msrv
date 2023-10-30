import pytest

from app.lib.hf.consts import Models, ReadAccessTokens
from app.lib.main import HFServiceCoordinator

API_KEY = ReadAccessTokens.FALLBACK_TOKEN_0
PROMPT_MODEL = Models.PROMPT
IMAGE_MODEL = Models.IMAGE


@pytest.mark.parametrize(
    "prompt, starter_hg_token, diffusion_model, prompt_model",
    [
        ("star trails over mountains", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("Ancient Transit in France", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("world war 2", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("roller-staker's rban flight", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("aerial autumn river.", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("rainbow dewdrops", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("the fashion of vacant places", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("george washington", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("ancient temple", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
        ("pharaoh", API_KEY, IMAGE_MODEL, PROMPT_MODEL),
    ],
)
def test_hf_service_coordinator(
    prompt, starter_hg_token, diffusion_model, prompt_model
):
    x = HFServiceCoordinator(
        prompt=prompt,
        starter_hg_token=starter_hg_token,
        diffusion_model=diffusion_model,
        prompt_model=prompt_model,
        use_prompt_enhancers=True,
    )
    generated_text = x.get_generated_text()
    raw_image = x.get_raw_image()

    assert isinstance(generated_text, str)
    assert isinstance(raw_image, bytes)
    # ImageSaver(raw_bytes=raw_image).save(output_file_name=uuid.uuid4().hex,folder='output')
