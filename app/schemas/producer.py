import re
from datetime import datetime
from typing import List, Optional, Union

from pydantic import (
    BaseModel,
    Field,
    field_serializer,
    field_validator,
    model_validator,
)


class ProducerBase(BaseModel):
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ do produtor")
    name: str = Field(..., min_length=1, max_length=255, description="Nome do produtor")
    farm_name: str = Field(..., min_length=1, max_length=255, description="Nome da fazenda")
    city: str = Field(..., min_length=1, max_length=100, description="Cidade")
    state: str = Field(..., min_length=2, max_length=2, description="Estado (sigla)")

    total_area_hectares: str = Field(
        ..., example="3,5 ha", description="Área total da fazenda (em hectares), ex: '3,5 ha'"
    )
    arable_area_hectares: str = Field(
        ..., example="1,7 ha", description="Área agricultável (em hectares), ex: '1,7 ha'"
    )
    vegetation_area_hectares: str = Field(
        ..., example="1,0 ha", description="Área de vegetação (em hectares), ex: '1,0 ha'"
    )

    planted_crops: Optional[str] = Field(None, description="Culturas plantadas")

    @field_validator("cpf_cnpj")
    @classmethod
    def validate_cpf_cnpj(cls, v: str) -> str:
        cpf_cnpj = re.sub(r"[^\d]", "", v)
        if len(cpf_cnpj) not in {11, 14}:
            raise ValueError("CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos")
        return cpf_cnpj

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: str) -> str:
        return v.upper()

    @field_validator("total_area_hectares", "arable_area_hectares", "vegetation_area_hectares")
    @classmethod
    def validate_hectares(cls, v: Union[float, str], info) -> float:
        """Converte valores de hectares de string ou float para float."""
        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith("ha"):
                v = v[:-2].strip().replace(",", ".")  # <- Ajuste feito aqui
            try:
                value = float(v)
            except ValueError:
                raise ValueError(f"Valor inválido para hectares: {v}. Use o formato '3,9 ha'")
        else:
            value = float(v)

        if value < 0:
            raise ValueError("Área não pode ser negativa")
        if info.field_name == "total_area_hectares" and value <= 0:
            raise ValueError("Área total deve ser maior que zero")
        return value

    @model_validator(mode="after")
    def validate_area_sum(self) -> "ProducerBase":
        total = self.total_area_hectares
        arable = self.arable_area_hectares
        vegetation = self.vegetation_area_hectares

        if total is not None and arable is not None and vegetation is not None:
            if arable + vegetation > total:
                raise ValueError("Área agricultável + vegetação não pode exceder a área total")
        return self


class ProducerCreate(ProducerBase):
    pass


class ProducerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    farm_name: Optional[str] = Field(None, min_length=1, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=2, max_length=2)
    total_area_hectares: Optional[Union[float, str]] = Field(
        None, description="Área total em hectares"
    )
    arable_area_hectares: Optional[Union[float, str]] = Field(
        None, description="Área agricultável em hectares"
    )
    vegetation_area_hectares: Optional[Union[float, str]] = Field(
        None, description="Área de vegetação em hectares"
    )
    planted_crops: Optional[str] = None

    @field_validator("state")
    @classmethod
    def validate_state(cls, v: Optional[str]) -> Optional[str]:
        return v.upper() if v is not None else v

    @field_validator("total_area_hectares", "arable_area_hectares", "vegetation_area_hectares")
    @classmethod
    def validate_hectares_update(cls, v: Optional[Union[float, str]], info) -> Optional[float]:
        """Converte valores de hectares para updates."""
        if v is None:
            return None

        if isinstance(v, str):
            v = v.strip().lower()
            if v.endswith("ha"):
                v = v[:-2].strip().replace(",", ".")  # <- Ajuste feito aqui
            try:
                value = float(v)
            except ValueError:
                raise ValueError(f"Valor inválido para hectares: {v}")
        else:
            value = float(v)

        if value < 0:
            raise ValueError("Área não pode ser negativa")
        if info.field_name == "total_area_hectares" and value <= 0:
            raise ValueError("Área total deve ser maior que zero")
        return value


class ProducerInDB(BaseModel):
    id: int
    cpf_cnpj: str
    name: str
    farm_name: str
    city: str
    state: str
    total_area_hectares: float
    arable_area_hectares: float
    vegetation_area_hectares: float
    planted_crops: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class ProducerResponse(ProducerInDB):
    @field_serializer(
        "total_area_hectares", "arable_area_hectares", "vegetation_area_hectares"
    )
    @staticmethod
    def serialize_hectares(v: float, _info) -> str:
        return f"{str(v).replace('.', ',')} ha"


class ProducerList(BaseModel):
    producers: List[ProducerResponse]
    total: int
    page: int
    size: int
