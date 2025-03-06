from textwrap import dedent
import yaml
import instructor
from openai import OpenAI

from record import DailyRecord

client = instructor.from_openai(OpenAI())

prompts = None

with open("prompts.yaml", "r") as file:
    try:
        prompts = yaml.safe_load(file)
        print(prompts)
    except yaml.YAMLError as exc:
        print(exc)


def refine_data_with_llm(data_list) -> list[str]:
    prompt = prompts["daily-report"]["prompt"]
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": dedent(prompt)
            },
            {"role": "user", "content": data_list},
        ],
        response_model=list[DailyRecord],
        model="gpt-4o-mini"
    )
    data = [str(record.record) for record in response]
    return data

def generate_weekly_summary(data: list[str]) -> str:
    prompt = prompts["weekly-report"]["prompt"]
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": dedent(prompt)
            },
            {"role": "user", "content": data},
        ],
        response_model=str,
        model="gpt-4o-mini"
    )
    return response

def generate_monthly_summary(data: list[str]) -> str:
    prompt = prompts["monthly-report"]["prompt"]
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": dedent(prompt)
            },
            {"role": "user", "content": data},
        ],
        response_model=str,
        model="gpt-4o-mini"
    )
    return response