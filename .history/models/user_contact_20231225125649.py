from config.database import Base
from sqlalchemy import Column, Integer, String, Float, VARCHAR, BIGINT, DATE, DateTime, Boolean, ForeignKey

# Definicion de una tabla
class Usuario(Base):
    __tablename__="Contacto"
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, nullable=False, ForeignKey("user.id", onupdate="CASCADE", ondelete="RESCTRICT"))     
    email = Column(VARCHAR(250), nullable=True) #varchar(250) NOT NULL,    
    fijo = Column(VARCHAR(20), nullable=True) #varchar(20) NOT NULL,        
    movil = Column(VARCHAR(20), nullable=True) #varchar(20) NOT NULL,        
    created = Column (DateTime, nullable=False) #datetime NOT NULL,    
    updated = Column (DateTime, nullable=False)  #datetime NOT NULL,
    creator_user= Column(BIGINT, nullable=False) #user BIGINT NOT NULL,     
    updater_user = Column(BIGINT, nullable=False) #user BIGINT NOT NULL,  