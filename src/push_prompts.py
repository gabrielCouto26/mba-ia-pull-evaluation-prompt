"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        description = prompt_data.get("description", "Prompt otimizado")
        techniques = prompt_data.get("techniques_applied", [])
        tags = prompt_data.get("tags", ["bug-to-user-story"])
        
        if techniques:
            description += f"\n\nTécnicas utilizadas: {', '.join(techniques)}"
            
        system_prompt = prompt_data.get("system_prompt", "")
        human_prompt = prompt_data.get("human_prompt", "{bug_report}")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_prompt)
        ])
        
        print(f"Fazendo push para o repositório '{prompt_name}' no LangSmith Hub...")
        url = hub.push(
            prompt_name,
            prompt,
            new_repo_is_public=True,
            new_repo_description=description,
            tags=tags
        )
        print(f"✅ Push realizado com sucesso! URL: {url}")
        return True
    except Exception as e:
        print(f"❌ Erro ao fazer push para o LangSmith: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1
        
    print_section_header("Iniciando push de prompts para o LangSmith")
    
    username_raw = os.getenv("USERNAME_LANGSMITH_HUB")
    username = username_raw.strip().replace(" ", "-").lower()
    
    prompt_file = "prompts/bug_to_user_story_v2.yml"
    print(f"Carregando arquivo {prompt_file}...")
    
    prompt_data = load_yaml(prompt_file)
    if not prompt_data:
        # Como o arquivo pode não existir ainda, apenas avisamos e encerramos
        return 1
        
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Validação do prompt falhou com os seguintes erros:")
        for error in errors:
            print(f"  - {error}")
        return 1
        
    prompt_name = f"{username}/bug_to_user_story_v2"
    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
