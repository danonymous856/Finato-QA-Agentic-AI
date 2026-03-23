from __future__ import annotations

from typing import List

from docx import Document

from models.schemas import Requirement, RequirementSource


def parse_brd_requirements(path: str) -> List[Requirement]:
    """
    Very lightweight BRD parser.

    This implementation is intentionally simple: it treats each non-empty
    paragraph as a requirement and looks for lines starting with 'AC:' as
    acceptance criteria. In a real system this would be replaced with a more
    sophisticated parser or an LLM-based extractor.
    """
    document = Document(path)
    requirements: List[Requirement] = []

    current_req_lines: List[str] = []
    current_ac: List[str] = []
    req_index = 1

    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            if current_req_lines:
                title = current_req_lines[0][:80]
                description = "\n".join(current_req_lines)
                requirements.append(
                    Requirement(
                        id=f"BRD_REQ_{req_index:03d}",
                        title=title,
                        description=description,
                        acceptance_criteria=current_ac,
                        source=RequirementSource.BRD,
                        source_ref=path,
                    )
                )
                req_index += 1
                current_req_lines = []
                current_ac = []
            continue

        if text.lower().startswith("ac:"):
            current_ac.append(text[3:].strip())
        else:
            current_req_lines.append(text)

    if current_req_lines:
        title = current_req_lines[0][:80]
        description = "\n".join(current_req_lines)
        requirements.append(
            Requirement(
                id=f"BRD_REQ_{req_index:03d}",
                title=title,
                description=description,
                acceptance_criteria=current_ac,
                source=RequirementSource.BRD,
                source_ref=path,
            )
        )

    return requirements

