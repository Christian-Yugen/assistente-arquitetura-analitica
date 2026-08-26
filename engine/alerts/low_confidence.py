from dataclasses import dataclass

@dataclass(frozen=True)
class LowConfidenceAlertProfile:
    independent_low_confidence_signal_count: int = 0
    human_confidence_confirmation_count: int = 0
    sensitive_signal_count: int = 0
    contract_error_count: int = 0

def classify_low_confidence_review(profile: LowConfidenceAlertProfile):
    if not (profile.independent_low_confidence_signal_count >= 1 and profile.human_confidence_confirmation_count == 0 and profile.sensitive_signal_count == 0 and profile.contract_error_count == 0):
        return None
    return {"rule_id":"ALT-LOWCONF-010","category":"alert","severity":"medium","title":"Baixa confiança acumulada exige revisão","description":"Um sinal independente e agregado exige confirmação humana.","evidence":[{"code":"EVD-ALT-LOWCONF-INDEPENDENT-SIGNAL","effect":"low_confidence_review_required","observed_value":profile.independent_low_confidence_signal_count,"expected_condition":"independent aggregated signal"}],"impact":"O resultado não deve orientar decisão até validação humana.","recommendation":"Confirmar a suficiência e o contexto analítico antes de usar o resultado.","question":{"text":"A confiança e o contexto analítico foram confirmados por responsável humano?","reason":"O alerta não calcula confiança nem usa conteúdo privado.","question_type":"single_choice","priority":"high","blocking":True,"options":[{"option_id":"confirm_confidence","label":"Confirmar confiança"},{"option_id":"defer_use","label":"Adiar uso"}],"affected_modules":["confidence","modeling"]}}
