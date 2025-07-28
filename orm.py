from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
from .config import settings

# Database connection string for PostgreSQL
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    ProductKey = Column(Integer, primary_key=True, index=True)
    Product_Name = Column(String, nullable=False)
    Brand = Column(String)
    Color = Column(String)
    Unit_Cost_USD = Column(Float)
    Unit_Price_USD = Column(Float)
    SubcategoryKey = Column(String)
    Subcategory = Column(String)
    CategoryKey = Column(String)
    Category = Column(String)

# To create tables in the database (run once)
def init_db():
    Base.metadata.create_all(bind=engine)

def import_products_from_csv(csv_path):
    session = SessionLocal()
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean and convert price fields
            unit_cost = float(row['Unit Cost USD'].replace('$','').replace(',','').strip()) if row['Unit Cost USD'] else None
            unit_price = float(row['Unit Price USD'].replace('$','').replace(',','').strip()) if row['Unit Price USD'] else None
            product = Product(
                ProductKey=int(row['ProductKey']),
                Product_Name=row['Product Name'],
                Brand=row['Brand'],
                Color=row['Color'],
                Unit_Cost_USD=unit_cost,
                Unit_Price_USD=unit_price,
                SubcategoryKey=row['SubcategoryKey'],
                Subcategory=row['Subcategory'],
                CategoryKey=row['CategoryKey'],
                Category=row['Category']
            )
            session.merge(product)  # merge to avoid duplicates on ProductKey
        session.commit()
    session.close()

