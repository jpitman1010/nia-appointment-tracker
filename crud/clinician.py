# crud/clinician.py

from sqlalchemy.orm import Session
from models.models import Provider
from schemas import ProviderCreate, ProviderUpdate
from utils import fuzzy_search_utils  # or wherever your fuzzy search function is
from crud.generic import search_entity  # Assuming your search function is here


def create_provider(db: Session, provider: ProviderCreate):
    # Check for existing similar providers using fuzzy search on first and last name
    query_str = f"{provider.fname} {provider.lname}"
    existing = search_entity(db.query(Provider), Provider, query=query_str, fields=["fname", "lname"])
    
    if existing:
        raise ValueError(f"A provider similar to '{provider.fname} {provider.lname}' already exists.")
    
    db_provider = Provider(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def update_provider(db: Session, provider_id: int, update_data: ProviderUpdate):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not db_provider:
        return None

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(db_provider, field, value)
    db.commit()
    db.refresh(db_provider)
    return db_provider


def delete_provider(db: Session, provider_id: int):
    db_provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if db_provider:
        db.delete(db_provider)
        db.commit()
    return db_provider


def get_provider_by_id(db: Session, provider_id: int):
    return db.query(Provider).filter(Provider.id == provider_id).first()


def get_all_providers(db: Session):
    return db.query(Provider).all()


def search_providers(db: Session, query: str):
    return search_providers(db.query(Provider), Provider, query, fields=["fname", "lname", "email"])
