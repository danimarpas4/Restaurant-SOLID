import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Load environment variables from .env file
load_dotenv()

# 2. Retrieve database credentials securely
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

# Initialize declarative base for ORM mapping
Base = declarative_base()

class Producto(Base):
    """
    Defines the immutable schema for 'Product' assets within the ecosystem.
    Acts as the single source of truth for item attributes and pricing.
    """
    __tablename__ = "productos"

    # Unique identifier for the asset (Primary Key)
    id = Column(Integer, primary_key=True)
    
    # Asset metadata definition
    nombre = Column(String(255), nullable=False)
    tipo = Column(String(255), nullable=False)
    
    # Valuation and status flags
    precio = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True)

    def __repr__(self):
        """
        Returns a string representation of the asset state for logging and debugging.
        """
        return (
            f"Producto(id={self.id}, nombre='{self.nombre}', "
            f"tipo='{self.tipo}', precio={self.precio}, disponible={self.disponible})"
        )

# --- Persistence Layer Configuration ---

# 3. Construct the secure Database Connection URL
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}"

# Engine initialization
engine = create_engine(DATABASE_URL)

# Schema Migration: Applies the defined schema to the target database instance
Base.metadata.create_all(engine)

# Session Factory: Handles the transactional scope for database operations
Session = sessionmaker(bind=engine)