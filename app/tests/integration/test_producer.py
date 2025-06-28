import pytest
from fastapi import status

MAX_ITEMS_PER_PAGE = 3
NOT_FOUND_ID = 9999
LIMIT = 5

payload = {
    "name": "Prod Teste",
    "cpf_cnpj": "12345678900",
    "address": "Rua Teste 123",
    "email": "teste@teste.com",
    "farm_name": "Fazenda Teste",
    "city": "São Paulo",
    "state": "SP",
    "total_area_hectares": "100.5",
    "arable_area_hectares": "80.0",
    "vegetation_area_hectares": "20.5",
}


@pytest.mark.anyio
async def test_create_producer(client):
    response = await client.post("/api/v1/producers/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data


@pytest.mark.anyio
async def test_get_producer(client):
    create_response = await client.post("/api/v1/producers/", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    producer_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/producers/{producer_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == payload["name"]


@pytest.mark.anyio
async def test_delete_producer(client):
    create_response = await client.post("/api/v1/producers/", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    producer_id = create_response.json()["id"]

    delete_response = await client.delete(f"/api/v1/producers/{producer_id}")
    assert delete_response.status_code == status.HTTP_200_OK

    get_response = await client.get(f"/api/v1/producers/{producer_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_update_producer(client):
    payload_local = {
        "name": "Prod Original",
        "cpf_cnpj": "22233344455",
        "farm_name": "Fazenda Original",
        "city": "Cidade A",
        "state": "SP",
        "total_area_hectares": "100.0",
        "arable_area_hectares": "60.0",
        "vegetation_area_hectares": "40.0",
    }
    create_response = await client.post("/api/v1/producers/", json=payload_local)
    assert create_response.status_code == status.HTTP_201_CREATED
    producer_id = create_response.json()["id"]

    update_payload = {"name": "Prod Atualizado", "planted_crops": "Milho"}

    update_response = await client.put(f"/api/v1/producers/{producer_id}", json=update_payload)
    assert update_response.status_code == status.HTTP_200_OK
    updated = update_response.json()
    assert updated["name"] == update_payload["name"]
    assert updated["planted_crops"] == update_payload["planted_crops"]


@pytest.mark.anyio
async def test_list_producers_with_pagination(client):
    for i in range(10):
        payload_local = {
            "name": f"Produtor {i}",
            "cpf_cnpj": f"0000000000{i}",
            "address": f"Rua {i}",
            "email": f"email{i}@teste.com",
            "farm_name": f"Fazenda {i}",
            "city": "Cidade X",
            "state": "SP",
            "total_area_hectares": "100.0",
            "arable_area_hectares": "80.0",
            "vegetation_area_hectares": "20.0",
        }
        response = await client.post("/api/v1/producers/", json=payload_local)
        assert response.status_code == status.HTTP_201_CREATED

    list_response = await client.get("/api/v1/producers/?skip=0&limit=3")
    assert list_response.status_code == status.HTTP_200_OK
    data = list_response.json()
    assert data["size"] == MAX_ITEMS_PER_PAGE
    assert len(data["producers"]) == MAX_ITEMS_PER_PAGE


@pytest.mark.anyio
async def test_get_nonexistent_producer(client):
    response = await client.get(f"/api/v1/producers/{NOT_FOUND_ID}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Producer not found" in response.json()["detail"]


@pytest.mark.anyio
async def test_update_nonexistent_producer(client):
    update_payload = {"name": "Inexistente Atualizado"}
    response = await client.put(f"/api/v1/producers/{NOT_FOUND_ID}", json=update_payload)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Producer not found."


@pytest.mark.anyio
async def test_list_producers_pagination_limits(client):
    for i in range(12):
        payload_local = {
            "name": f"Produtor {i}",
            "cpf_cnpj": f"{i:011d}",
            "farm_name": f"Fazenda {i}",
            "city": "Cidade X",
            "state": "SP",
            "total_area_hectares": "100,0 ha",
            "arable_area_hectares": "80,0 ha",
            "vegetation_area_hectares": "20,0 ha",
        }
        response = await client.post("/api/v1/producers/", json=payload_local)
        assert response.status_code == status.HTTP_201_CREATED

    response = await client.get(f"/api/v1/producers/?skip=5&limit={LIMIT}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert len(data["producers"]) <= LIMIT
