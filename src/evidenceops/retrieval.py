from __future__ import annotations

import math
import re
from collections import Counter
from collections.abc import Iterable

from .models import Citation, Contradiction, EvidenceChecks, StoredChunk


TOKEN_PATTERN = re.compile(r"[a-z0-9]+|[\u4e00-\u9fff]", re.IGNORECASE)
SENTENCE_PATTERN = re.compile(r"(?<=[.!?。！？])\s+|\n+")
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does", "for", "from", "how",
    "in", "is", "it", "of", "on", "or", "our", "please", "that", "the", "their", "this", "to", "what",
    "when", "where", "which", "who", "will", "with", "your",
}
NEGATIVE = {
    "no", "not", "never", "none", "disabled", "false", "without", "cannot", "isn't", "isnt", "doesn't",
    "doesnt", "不", "未", "无", "否",
}
POSITIVE = {"yes", "enabled", "true", "always", "supports", "implemented", "有", "是", "已", "支持"}
MEASURE_PATTERN = re.compile(
    r"\b(\d+(?:\.\d+)?)\s*(hours?|hrs?|days?|minutes?|mins?|seconds?|secs?|%)\b",
    re.IGNORECASE,
)
GENERIC_QUERY_TERMS = {
    "compliant", "confirm", "control", "controls", "current", "data", "describe", "detail", "enabled", "explain",
    "implemented", "information", "list", "policy", "process", "production", "provide", "security", "state",
    "support", "supports", "system",
}
TOKEN_ALIASES = {
    "annually": "annual",
    "encrypted": "encrypt",
    "encrypts": "encrypt",
    "encryption": "encrypt",
    "models": "model",
    "notification": "notify",
    "notified": "notify",
    "regions": "region",
    "stored": "store",
    "storage": "store",
    "trained": "train",
    "training": "train",
}


def _normalize_token(token: str) -> str:
    normalized = token.casefold()
    if normalized in TOKEN_ALIASES:
        return TOKEN_ALIASES[normalized]
    if len(normalized) > 4 and normalized.endswith("s") and not normalized.endswith("ss"):
        return normalized[:-1]
    return normalized


def tokenize(text: str) -> list[str]:
    return [
        _normalize_token(token)
        for token in TOKEN_PATTERN.findall(text)
        if token.casefold() not in STOPWORDS
    ]


def _best_quote(question: str, text: str, max_chars: int = 420) -> str:
    question_tokens = set(tokenize(question))
    sentences = [
        (index, sentence.strip())
        for index, sentence in enumerate(SENTENCE_PATTERN.split(text))
        if sentence.strip()
        and not sentence.lstrip().startswith("#")
        and not re.match(r"^(document owner|approved|classification|status):", sentence.strip(), re.IGNORECASE)
    ]
    if not sentences:
        return text[:max_chars].strip()
    ranked = sorted(
        sentences,
        key=lambda item: len(question_tokens.intersection(tokenize(item[1]))),
        reverse=True,
    )
    selected = [ranked[0]]
    covered = question_tokens.intersection(tokenize(ranked[0][1]))
    for candidate in ranked[1:]:
        added = question_tokens.intersection(tokenize(candidate[1])) - covered
        combined = " ".join(sentence for _, sentence in sorted([*selected, candidate]))
        if added and len(combined) <= max_chars:
            selected.append(candidate)
            covered.update(added)
        if len(selected) == 2 or covered == question_tokens:
            break
    quote = " ".join(sentence for _, sentence in sorted(selected))
    return quote[:max_chars].rstrip()


def retrieve(question: str, chunks: Iterable[StoredChunk], top_k: int = 4) -> list[Citation]:
    chunk_list = list(chunks)
    query_counts = Counter(tokenize(question))
    if not query_counts or not chunk_list:
        return []
    document_frequency: Counter[str] = Counter()
    tokenized_chunks: list[list[str]] = []
    for chunk in chunk_list:
        tokens = tokenize(chunk.text)
        tokenized_chunks.append(tokens)
        document_frequency.update(set(tokens))
    scored: list[tuple[float, StoredChunk]] = []
    for chunk, tokens in zip(chunk_list, tokenized_chunks, strict=True):
        counts = Counter(tokens)
        distinctive_query_tokens = set(query_counts) - GENERIC_QUERY_TERMS
        required_matches = max(1, math.ceil(len(distinctive_query_tokens) * 0.35))
        if distinctive_query_tokens and len(distinctive_query_tokens.intersection(counts)) < required_matches:
            continue
        score = 0.0
        for token, query_frequency in query_counts.items():
            if token not in counts:
                continue
            inverse_document_frequency = math.log((len(chunk_list) + 1) / (document_frequency[token] + 0.5)) + 1
            score += min(counts[token], 3) * query_frequency * inverse_document_frequency
        normalizer = math.sqrt(max(len(set(tokens)), 1) * max(len(query_counts), 1))
        normalized = score / normalizer
        if normalized > 0:
            scored.append((normalized, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    if not scored:
        return []
    best_score = scored[0][0]
    citations: list[Citation] = []
    for score, chunk in scored[:top_k]:
        if score < max(0.15, best_score * 0.18):
            continue
        citations.append(
            Citation(
                document=chunk.document,
                page_or_sheet=chunk.page_or_sheet,
                quote=_best_quote(question, chunk.text),
                document_id=chunk.document_id,
                chunk_id=chunk.id,
                relevance_score=round(score, 4),
            )
        )
    return citations


def detect_contradictions(citations: list[Citation]) -> list[Contradiction]:
    contradictions: list[Contradiction] = []
    for left_index, left in enumerate(citations):
        left_tokens = set(tokenize(left.quote))
        left_negative = bool(left_tokens.intersection(NEGATIVE))
        left_positive = bool(left_tokens.intersection(POSITIVE))
        left_measures = {(value, unit.casefold().rstrip("s")) for value, unit in MEASURE_PATTERN.findall(left.quote)}
        for right_index in range(left_index + 1, len(citations)):
            right = citations[right_index]
            right_tokens = set(tokenize(right.quote))
            right_negative = bool(right_tokens.intersection(NEGATIVE))
            right_positive = bool(right_tokens.intersection(POSITIVE))
            right_measures = {
                (value, unit.casefold().rstrip("s")) for value, unit in MEASURE_PATTERN.findall(right.quote)
            }
            overlap = left_tokens.intersection(right_tokens) - NEGATIVE - POSITIVE
            topic_ratio = len(overlap) / max(min(len(left_tokens), len(right_tokens)), 1)
            opposite = (left_negative and not right_negative and right_positive) or (
                right_tokens.intersection(NEGATIVE) and not left_negative and left_positive
            )
            shared_units = {unit for _, unit in left_measures}.intersection(unit for _, unit in right_measures)
            numeric_conflict = any(
                {value for value, measure_unit in left_measures if measure_unit == unit}
                != {value for value, measure_unit in right_measures if measure_unit == unit}
                for unit in shared_units
            )
            if topic_ratio >= 0.25 and (opposite or numeric_conflict):
                contradictions.append(
                    Contradiction(
                        summary=(
                            f"Potential conflict between {left.document} ({left.page_or_sheet}) and "
                            f"{right.document} ({right.page_or_sheet})."
                        ),
                        citation_indexes=[left_index, right_index],
                    )
                )
    return contradictions


def analyze_grounding(answer: str | None, citations: list[Citation]) -> EvidenceChecks:
    contradictions = detect_contradictions(citations)
    if not answer or not citations:
        return EvidenceChecks(
            grounded=False,
            hallucination_risk=bool(answer),
            unsupported_claims=[answer] if answer else [],
            contradictions=contradictions,
        )
    evidence_text = "\n".join(citation.quote for citation in citations)
    evidence_normalized = re.sub(r"\s+", " ", evidence_text).casefold()
    evidence_tokens = set(tokenize(evidence_text))
    unsupported: list[str] = []
    for sentence in [item.strip() for item in SENTENCE_PATTERN.split(answer) if item.strip()]:
        normalized = re.sub(r"\s+", " ", sentence).casefold().strip(' \"\'')
        if normalized.startswith(("the evidence states:", "evidence excerpt:", "available evidence states:")):
            normalized = normalized.split(":", 1)[1].strip(' \"\'')
        if normalized and normalized in evidence_normalized:
            continue
        material_tokens = set(tokenize(sentence))
        numbers = set(re.findall(r"\b\d+(?:\.\d+)?%?\b", sentence))
        best_citation = max(
            citations,
            key=lambda citation: len(material_tokens.intersection(tokenize(citation.quote))),
        )
        best_tokens = set(tokenize(best_citation.quote))
        best_numbers = set(re.findall(r"\b\d+(?:\.\d+)?%?\b", best_citation.quote))
        polarity_mismatch = bool(material_tokens.intersection(NEGATIVE)) != bool(best_tokens.intersection(NEGATIVE))
        coverage = len(material_tokens.intersection(evidence_tokens)) / max(len(material_tokens), 1)
        if polarity_mismatch or numbers - best_numbers or (material_tokens and coverage < 0.72):
            unsupported.append(sentence)
    return EvidenceChecks(
        grounded=not unsupported,
        hallucination_risk=bool(unsupported),
        unsupported_claims=unsupported,
        contradictions=contradictions,
    )
