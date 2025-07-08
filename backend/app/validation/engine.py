import json
import asyncio
from typing import List, Dict, Any
from datetime import datetime

from app.schemas import ValidationResult, ValidationError, ClauseMatch, Severity
from app.utils.validation_helpers import chunk_text
from app.utils.clause_matcher import FaissClauseMatcher
from app.utils.critical_clause_detector import detect_critical_clauses, build_validation_prompt

class TermsheetValidationEngine:
    """
    Orchestrates the validation process for termsheets by combining
    rule-based validation, LLM-based validation, and clause matching.
    """
    
    def __init__(self, reference_clauses: List[str]):
        """
        Initialize the validation engine with reference clauses.
        
        Args:
            reference_clauses: List of standard clauses to match against
        """
        from app.crud.validation_ops import ValidationOperations
        
        self.rule_validator = ValidationOperations()
        self.reference_clauses = reference_clauses

    async def validate(self, termsheet_data: Dict[str, Any], text: str) -> ValidationResult:
        """
        Perform comprehensive validation of a termsheet.
        
        Args:
            termsheet_data: Structured data extracted from the termsheet
            text: Raw text of the termsheet
            
        Returns:
            ValidationResult with errors, criticality score, and clause matches
        """
        # 1. Rule-based validation
        rule_result = self.rule_validator.validate_termsheet(termsheet_data)
        
        # 2. LLM validation
        from app.routers.validate import TermsheetValidator
        validator = TermsheetValidator()
        llm_result = await validator.validate_with_ollama(text)
        
        # 3. Clause-level matching
        matcher = FaissClauseMatcher(self.reference_clauses)
        chunks = chunk_text(text)
        clause_matches = matcher.match(chunks)
        
        # 4. Add critical clause detection
        critical_result = detect_critical_clauses(chunks)
        
        # 5. Combine errors from all sources
        errors = []
        
        # Add rule-based errors
        if isinstance(rule_result, dict) and "errors" in rule_result:
            errors.extend(rule_result["errors"])
        
        # Add LLM-based errors
        if isinstance(llm_result, dict) and "errors" in llm_result:
            errors.extend(llm_result["errors"])
        
        # Add errors from missing critical clauses
        critical_clauses_missing = any(
            cm.match_type == "missing" and any(keyword in cm.clause.lower() for keyword in 
                ["interest rate", "maturity", "redemption", "collateral"])
            for cm in clause_matches
        )
        
        if critical_clauses_missing:
            errors.append(ValidationError(
                type="MISSING_CLAUSE",
                description="Critical clause missing or significantly different from standard",
                section="Document",
                severity=Severity.CRITICAL
            ))
        
        # If critical clauses found, add to validation summary and errors
        if critical_result["is_critical"]:
            errors.append(ValidationError(
                type="CRITICAL_CLAUSE",
                description="Document contains critical financial clauses requiring review",
                section="Financial Terms",
                severity=Severity.HIGH
            ))
        
        # 6. Calculate overall criticality score
        rule_criticality = rule_result.get("criticality_score", 0) if isinstance(rule_result, dict) else 0
        llm_criticality = llm_result.get("criticality_score", 0) if isinstance(llm_result, dict) else 0
        
        criticality_score = max(rule_criticality, llm_criticality)
        if critical_clauses_missing:
            criticality_score = max(criticality_score, 90)  # High criticality for missing clauses
        if critical_result["is_critical"]:
            criticality_score = max(criticality_score, 85)  # High criticality for critical clauses
        
        # 7. Create validation summary
        validation_summary = llm_result.get("validation_summary", "") if isinstance(llm_result, dict) else ""
        if not validation_summary:
            validation_summary = "Document validation complete."
            if errors:
                validation_summary += f" Found {len(errors)} issues."
        
        # Add critical clause information to summary
        if critical_result["is_critical"]:
            validation_summary += f" Document contains {len(critical_result['critical_chunks'])} critical clauses."
            
            # Optional: Validate critical clauses with LLM
            prompt = build_validation_prompt(critical_result["critical_chunks"])
            # You can call your LLM here if needed
            # critical_llm_result = await validator.validate_with_ollama(prompt)
            # if critical_llm_result and "validation_summary" in critical_llm_result:
            #     validation_summary += f" Critical clause analysis: {critical_llm_result['validation_summary']}"
        
        return ValidationResult(
            errors=errors,
            criticality_score=criticality_score,
            validation_summary=validation_summary,
            clause_matches=clause_matches
        )
