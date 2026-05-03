"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

# import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    prompt = hub.pull("leonanluppi/bug_to_user_story_v1")
    return prompt


def main():
    """Função principal"""
    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1
    print_section_header("Iniciando pull de prompts do LangSmith")
    prompt = pull_prompts_from_langsmith()
    save_yaml(prompt, Path("prompts/bug_to_user_story_v1.yml"))
    print("Pull de prompts concluído com sucesso!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
