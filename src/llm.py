import os
from textwrap import dedent

import instructor
import yaml
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam, \
    ChatCompletionContentPartTextParam
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

from record import DailyRecord

load_dotenv()

client = instructor.from_openai(
    OpenAI(
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=createHeaders(
            virtual_key=os.getenv("VIRTUAL_KEY"),
            api_key=os.getenv("PORTKEY_API_KEY"),
            config={
                "cache": {
                    "mode": "simple"
                },
            }
        )
    )
)

prompts = None

with open("../prompts.yml", "r") as file:
    try:
        prompts = yaml.safe_load(file)
        print(prompts)
    except yaml.YAMLError as exc:
        print(exc)


def refine_data_with_llm(data_list: list[ChatCompletionContentPartTextParam]) -> list[str]:
    prompt = prompts["daily-report"]["prompt"]
    response = client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                content=dedent(prompt),
                role="system"
            ),
            ChatCompletionUserMessageParam(
                content=data_list,
                role="user"
            )
        ],
        response_model=list[DailyRecord],
        model=os.getenv("MODEL")
    )
    data = [str(record.record) for record in response]
    return data


def generate_weekly_summary(data: list[ChatCompletionContentPartTextParam]) -> str:
    prompt = prompts["weekly-report"]["prompt"]
    response = client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                content=dedent(prompt),
                role="system"
            ),
            ChatCompletionUserMessageParam(
                content=data,
                role="user"
            )
        ],
        response_model=str,
        model=os.getenv("MODEL")
    )
    return response


def generate_monthly_summary(data: list[ChatCompletionContentPartTextParam]) -> str:
    prompt = prompts["monthly-report"]["prompt"]
    response = client.chat.completions.create(
        messages=[
            ChatCompletionSystemMessageParam(
                content=dedent(prompt),
                role="system"
            ),
            ChatCompletionUserMessageParam(
                content=data,
                role="user"
            )
        ],
        response_model=str,
        model=os.getenv("MODEL")
    )
    return response