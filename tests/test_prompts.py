"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture
def prompt_data():
    prompt_file = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
    try:
        data = load_prompts(str(prompt_file))
        # Se for um objeto Langchain carregado via yaml.unsafe_load, vamos extrair seu dict interno
        if hasattr(data, '__dict__'):
            data = data.__dict__
        return data
    except FileNotFoundError:
        pytest.fail(f"Arquivo não encontrado: {prompt_file}")
    except Exception as e:
        pytest.fail(f"Erro ao carregar o arquivo YAML: {e}")

class TestPrompts:
    def test_prompt_has_system_prompt(self, prompt_data):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        is_valid, errors = validate_prompt_structure(prompt_data)
        assert is_valid, f"Estrutura do prompt inválida: {', '.join(errors)}"

    def test_prompt_has_role_definition(self, prompt_data):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        role_keywords = ["você é", "atue como", "aja como", "você atua como", "persona:", "papel:"]
        assert any(keyword in system_prompt for keyword in role_keywords), "Nenhuma definição de persona encontrada no system_prompt"

    def test_prompt_mentions_format(self, prompt_data):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        format_keywords = ["markdown", "user story", "formato"]
        assert any(keyword in system_prompt for keyword in format_keywords), "Prompt não exige formato Markdown ou User Story explícito"

    def test_prompt_has_few_shot_examples(self, prompt_data):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = prompt_data.get("system_prompt", "").lower()
        example_keywords = ["exemplo", "example", "saída esperada", "entrada:", "saída:"]
        assert any(keyword in system_prompt for keyword in example_keywords), "Nenhum exemplo few-shot encontrado no prompt"

    def test_prompt_no_todos(self, prompt_data):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = prompt_data.get("system_prompt", "")
        assert "TODO" not in system_prompt, "O prompt ainda contém 'TODO'"

    def test_minimum_techniques(self, prompt_data):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = prompt_data.get("techniques_applied", [])
        assert isinstance(techniques, list), "'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, f"Mínimo de 2 técnicas requeridas, mas apenas {len(techniques)} encontradas"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])