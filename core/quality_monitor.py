import logging
import json
from dataclasses import dataclass, field
from typing import List
from domain.models import AgentState

logger = logging.getLogger("agentcore.quality")

@dataclass
class QualityMetrics:
    response_length: int
    steps_used: int
    max_steps: int
    elapsed_seconds: float
    has_errors: bool

@dataclass  
class QualityThresholds:
    min_response_length: int = 50
    max_steps_ratio: float = 0.8    # alerta si usa más del 80% de los steps
    max_elapsed_seconds: float = 30.0
    max_error_rate: float = 0.1     # alerta si más del 10% de runs tienen errores

class QualityMonitor:
    def __init__(self, thresholds: QualityThresholds = None):
        self.thresholds = thresholds or QualityThresholds()
        self.recent_runs: List[QualityMetrics] = []
    
    def record(self, state: AgentState, elapsed_seconds: float) -> None:
        metrics = QualityMetrics(
            response_length=len(state.final_answer or ""),
            steps_used=len(state.steps),
            max_steps=5,
            elapsed_seconds=elapsed_seconds,
            has_errors=len(state.errors) > 0 if hasattr(state, 'errors') else False
        )
        self.recent_runs.append(metrics)
        self._check_alerts(metrics)
    
    def _check_alerts(self, metrics: QualityMetrics) -> None:
        # Implementá las 4 alertas según los thresholds
        if metrics.response_length< self.thresholds.min_response_length:
            logger.warning(json.dumps({
                "event": "quality_alert",
                "type": "response_too_short",
                "value": metrics.response_length,
                "threshold": self.thresholds.min_response_length
            }))
        if metrics.steps_used / metrics.max_steps > self.thresholds.max_steps_ratio:
            logger.warning(json.dumps({
                            "event": "quality_alert",
                            "type": "response_max_steps_ratio_exceeded",
                            "value": metrics.max_steps,
                            "threshold": self.thresholds.max_steps_ratio
                        }))
            logger.warning(f"Steps used {metrics.steps_used} exceeds threshold ratio {self.thresholds.max_steps_ratio}")
        if metrics.elapsed_seconds> self.thresholds.max_elapsed_seconds:
            logger.warning(json.dumps({
                            "event": "quality_alert",
                            "type": "response_Max_seconds_exceeded",
                            "value": metrics.elapsed_seconds,
                            "threshold": self.thresholds.max_elapsed_seconds
                        }))
        if self._error_rate() > self.thresholds.max_error_rate:
            logger.warning(json.dumps({
                            "event": "quality_alert",
                            "type": "max_error_rate_exceeded",
                            "value": metrics.has_errors,
                            "threshold": self.thresholds.max_error_rate
                        }))
        
        pass
    
    def _error_rate(self) -> float:
        # Calculá la tasa de errores de los últimos runs
        losultimos_20 = self.recent_runs[-20:]
        state_with_errors= sum(1 for run in losultimos_20 if run.has_errors)
        return state_with_errors/len(losultimos_20) if losultimos_20 else 0.0