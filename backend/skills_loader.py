import os
import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class SkillMetadata:
    def __init__(self, name: str, description: str, body: str, file_path: str):
        self.name = name
        self.description = description
        self.body = body.strip()
        self.file_path = file_path

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "system_prompt": self.body,
            "file_path": str(self.file_path)
        }

class SkillsLoader:
    """
    Dynamically loads and parses Autonomous Specialist Agent SKILL.md files from .agents/skills/
    Extracts YAML frontmatter (metadata) and markdown body (system instructions),
    ensuring runtime agents stay 100% faithful to the specialist agent skill specs.
    """
    def __init__(self, skills_root: Optional[Path] = None):
        if skills_root is None:
            # Check both workspace root and backend root
            backend_dir = Path(__file__).resolve().parent
            candidates = [
                backend_dir.parent / ".agents" / "skills",
                backend_dir / ".agents" / "skills",
            ]
            self.skills_root = candidates[0]
            for c in candidates:
                if c.exists():
                    self.skills_root = c
                    break
        else:
            self.skills_root = Path(skills_root)
        
        self.skills: Dict[str, SkillMetadata] = {}
        self.load_all_skills()

    def load_all_skills(self) -> Dict[str, SkillMetadata]:
        self.skills.clear()
        
        # Search primary and fallback roots
        candidates = [self.skills_root]
        backend_dir = Path(__file__).resolve().parent
        if backend_dir / ".agents" / "skills" not in candidates:
            candidates.append(backend_dir / ".agents" / "skills")
        if backend_dir.parent / ".agents" / "skills" not in candidates:
            candidates.append(backend_dir.parent / ".agents" / "skills")

        loaded = False
        for root in candidates:
            if root.exists():
                for skill_dir in root.iterdir():
                    if skill_dir.is_dir():
                        skill_file = skill_dir / "SKILL.md"
                        if skill_file.exists():
                            skill = self._parse_skill_file(skill_file)
                            if skill:
                                self.skills[skill.name] = skill
                                loaded = True
                if loaded:
                    break
        
        if not loaded:
            print(f"[SkillsLoader] Warning: Specialist agent skills root not found across candidates.")
        else:
            print(f"[SkillsLoader] Successfully loaded {len(self.skills)} specialist skills: {list(self.skills.keys())}")
        return self.skills

    def _parse_skill_file(self, file_path: Path) -> Optional[SkillMetadata]:
        try:
            content = file_path.read_text(encoding="utf-8")
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
            if match:
                frontmatter_raw = match.group(1)
                body = match.group(2)
                metadata = yaml.safe_load(frontmatter_raw) or {}
                name = metadata.get("name", file_path.parent.name)
                description = metadata.get("description", "")
                return SkillMetadata(name=name, description=description, body=body, file_path=str(file_path))
            else:
                name = file_path.parent.name
                return SkillMetadata(name=name, description="", body=content, file_path=str(file_path))
        except Exception as e:
            print(f"[SkillsLoader] Error parsing {file_path}: {e}")
            return None

    def get_skill(self, name: str) -> Optional[SkillMetadata]:
        return self.skills.get(name)

    def get_prompt(self, name: str) -> str:
        skill = self.get_skill(name)
        if skill:
            return skill.body
        return f"System prompt for skill '{name}' not found."

    def list_skills(self) -> Dict[str, Any]:
        return {name: skill.to_dict() for name, skill in self.skills.items()}

# Global singleton
skills_registry = SkillsLoader()
