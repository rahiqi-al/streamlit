from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime,and_,or_,cast
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker 
import pandas as pd
from datetime import date
from config.config import config
import streamlit as st



def extract_orm(session,Base,engine,min_price,max_price,min_rooms,max_rooms,min_baths,max_bath,ville,equipements,start_date,end_date):

    class AnnonceEquipement(Base):
        __tablename__ = 'annonce_equipement'
        
        annonce_id = Column(Integer, ForeignKey('annonces.id'), primary_key=True)
        equipement_id = Column(Integer, ForeignKey('equipements.id'), primary_key=True)
        
        annonce = relationship("Annonce", back_populates="equipements")
        equipement = relationship("Equipement", back_populates="annonces")

    class Annonce(Base):
        __tablename__ = 'annonces'
        
        id = Column(Integer, primary_key=True)
        title = Column(String)
        price = Column(String)  
        datetime = Column(DateTime, nullable=False)
        nb_rooms = Column(Integer)
        nb_baths = Column(Integer)
        surface_area = Column(Float)
        link = Column(String)
        city_id = Column(Integer, ForeignKey('villes.id'), nullable=False)
        
        ville = relationship("Ville", back_populates="annonces")
        equipements = relationship("AnnonceEquipement", back_populates="annonce")

    class Ville(Base):
        __tablename__ = 'villes'
        
        id = Column(Integer, primary_key=True)
        name = Column(String)
        
        annonces = relationship("Annonce", back_populates="ville")

    class Equipement(Base):
        __tablename__ = 'equipements'
        
        id = Column(Integer, primary_key=True)
        name = Column(String)
        
        annonces = relationship("AnnonceEquipement", back_populates="equipement")


    Base.metadata.create_all(engine)


    filted_obj = (session.query(Annonce,Ville,AnnonceEquipement,Equipement).join(Ville ,Ville.id==Annonce.city_id).join
    (AnnonceEquipement ,AnnonceEquipement.annonce_id==Annonce.id).join(Equipement,Equipement.id==AnnonceEquipement.equipement_id).filter(
        and_(


            cast(Annonce.price, Integer) >= min_price,
            cast(Annonce.price, Integer) <= max_price,
            Annonce.nb_rooms >= min_rooms,
            Annonce.nb_rooms <= max_rooms,
            Annonce.nb_baths >= min_baths,
            Annonce.nb_baths <= max_bath,
            Annonce.datetime >= start_date,  
            Annonce.datetime <= end_date,
            Ville.name == ville,
            or_(Equipement.name.in_(equipements) , (len(equipements) == 0))

        )

    ).all())

    data = []
    for obj in filted_obj:
        # Convert each tuple of ORM objects into a dictionary
        annonce, ville, annonce_equipement, equipement = obj
        row = {
            'annonce_id': annonce.id,
            'title': annonce.title,
            'price': annonce.price,
            'datetime': annonce.datetime,
            'surface_area': annonce.surface_area,
            'nb_rooms': annonce.nb_rooms,
            'nb_baths': annonce.nb_baths,
            'link': annonce.link,
            'ville_name': ville.name,
            'equipement_name': equipement.name,
        }
        data.append(row)

    return pd.DataFrame(data)










