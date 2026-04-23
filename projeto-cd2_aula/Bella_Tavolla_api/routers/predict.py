from fastapi import APIRouter
from pydantic import BaseModel, Field
import numpy as np

router = APIRouter()

# Seu repositório exato da aula
REPO_ID = "joaogabriel101735/puc-sp-aula"
_model = None

def get_model():
    global _model
    if _model is None:
        from model_utils import load_model
        _model = load_model(REPO_ID)
    return _model

class PredictInput(BaseModel):
    custo_prato: float = Field(gt=0, description="Valor de custo dos insumos")
    dia_da_semana: int = Field(ge=0, le=6, description="Dia da semana (0-6)")
    hora_pedido: int = Field(ge=0, le=23, description="Hora do dia (0-23)")
    tempo_mesa: int = Field(ge=0, description="Estimativa de tempo de ocupação (min)")
    popularidade: float = Field(ge=1, le=5, description="Nota média do prato (1-5)")

class PredictOutput(BaseModel):
    prediction: int
    probability: float
    label: str
    model_version: str

@router.post("/predict", response_model=PredictOutput)
async def predict(input: PredictInput):
    model = get_model()

    # A ordem aqui é idêntica à do treino
    features = np.array([[
        input.custo_prato,
        input.dia_da_semana,
        input.hora_pedido,
        input.tempo_mesa,
        input.popularidade
    ]])

    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])
    label = "alta demanda" if prediction == 1 else "baixa demanda"

    return PredictOutput(
        prediction=prediction,
        probability=round(probability, 4),
        label=label,
        model_version=REPO_ID
    )