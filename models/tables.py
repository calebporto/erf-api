from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import ARRAY, JSON

Base = declarative_base()

class Person(Base):
    r'''
    Classe universal para cadastro de usuários, seja PF ou PJ.
    :doctype serve para indicar o tipo de pessoa, sendo:
    - 1 para pessoa física
    - 2 para pessoa jurídica.
    :persontype indica o tipo de usuário, sendo:
    - 1 para administrador
    - 2 para secretário administrativo
    - 3 para vendedor
    - 4 para cliente
    - 5 para contador
    :is_active indica se o usuário está permitido a acessar a plataforma no caso de
    vendedo, funcionário e contador, e se está permitido a fazer novas compras no caso de clientes.
    '''
    __tablename__ = 'person'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    alternative_id = Column(String, unique=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    user_name = Column(String, unique=True)
    hash = Column(String)
    doctype = Column(Integer, nullable=False)
    persontype = Column(ARRAY(Integer), nullable=False)
    is_active = Column(Boolean, nullable=False)
    person_pf_data_person_id = relationship("Person_PF_Data")
    person_pj_data_person_id = relationship("Person_PJ_Data")
    sale_client_id = relationship("Sale", foreign_keys="Sale.client_id")
    sale_salesman_id = relationship("Sale", foreign_keys="Sale.salesman_id")
    error_logs_user_id = relationship("Error_Logs")
    access_user_id = relationship("Access")

    def __init__(self, alternative_id, name, email, user_name, hash, doctype, persontype, is_active):
        self.alternative_id = alternative_id
        self.name = name
        self.email = email
        self.user_name = user_name
        self.hash = hash
        self.doctype = doctype
        self.persontype = persontype
        self.is_active = is_active

class Person_PF_Data(Base):
    __tablename__ = 'person_pf_data'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id), unique=True, nullable=False)
    cpf = Column(String, nullable=False, unique=True)
    gender = Column(String, nullable=False)
    cep = Column(String, nullable=False)
    public_place = Column(String, nullable=False)
    place_number = Column(String, nullable=False)
    complement = Column(String)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    uf = Column(String, nullable=False)
    tel = Column(String, nullable=False)
    birth = Column(Date, nullable = False)

    def __init__(self, person_id, cpf, gender, cep, public_place, place_number, complement, district, city, uf, tel, birth):
        self.person_id = person_id
        self.cpf = cpf
        self.gender = gender
        self.cep = cep
        self.public_place = public_place
        self.place_number = place_number
        self.complement = complement
        self.district = district
        self.city = city
        self.uf = uf
        self.tel = tel
        self.birth = birth

class Person_PJ_Data(Base):
    __tablename__ = 'person_pj_data'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id), unique=True, nullable=False)
    cnpj = Column(String, nullable=False, unique=True)
    cp_name = Column(String, nullable=False, unique=True)
    ie = Column(String, unique=True)
    tel = Column(String, nullable=False, unique=True)
    public_place = Column(String, nullable=False)
    place_number = Column(String, nullable=False)
    complement = Column(String)
    district = Column(String, nullable=False)
    city = Column(String, nullable=False)
    uf = Column(String, nullable=False)
    cep = Column(String, nullable=False)

    def __init__(self, person_id, cnpj, cp_name, ie, tel, public_place, place_number, complement, district, city, uf, cep):
        self.person_id = person_id
        self.cnpj = cnpj
        self.cp_name = cp_name
        self.ie = ie
        self.tel = tel
        self.public_place = public_place
        self.place_number = place_number
        self.complement = complement
        self.district = district
        self.city = city
        self.uf = uf
        self.cep = cep

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=False)
    ean = Column(String)
    weight = Column(Float, nullable=False)
    inventory = Column(Integer)
    is_active = Column(Boolean, nullable=False)
    item_simple_data_id = relationship("Item_Simple_Data")
    item_tax_data_id = relationship("Item_Tax_Data")

    def __init__(self, name, price, ean, weight, inventory, is_active):
        self.name = name
        self.price = price
        self.ean = ean
        self.weight = weight
        self.inventory = inventory
        self.is_active = is_active

class Item_Simple_Data(Base):
    __tablename__ = 'item_simple_data'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    item_id = Column(Integer, ForeignKey(Item.id), unique=True, nullable=False)
    cost = Column(Float)
    brand = Column(String)
    category = Column(String)
    image_id = Column(String)

    def __init__(self, item_id, cost, brand, category, image_id):
        self.item_id = item_id
        self.cost = cost
        self.brand = brand
        self.category = category
        self.image_id = image_id


class Item_Tax_Data(Base):
    __tablename__ = 'item_tax_data'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    item_id = Column(Integer, ForeignKey(Item.id), unique=True, nullable=False)
    ncm = Column(String, nullable=False)
    measure = Column(String, nullable=False)
    origin = Column(Integer, nullable=False)
    discount = Column(Float)
    cest = Column(String)
    
    def __init__(self, item_id, ncm, measure, origin, discount, cest):
        self.item_id = item_id
        self.ncm = ncm
        self.measure = measure
        self.origin = origin
        self.discount = discount
        self.cest = cest

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    client_id = Column(Integer, ForeignKey(Person.id, ondelete='SET NULL'))
    salesman_id = Column(Integer, ForeignKey(Person.id, ondelete='SET NULL'))
    item_list = Column(JSON, nullable=False)
    sale_date = Column(Date, nullable=False)
    total = Column(Float, nullable=False)
    image_id = Column(String)
    pay_type = Column(String, nullable=False)
    pay_term = Column(String)
    is_paid = Column(Boolean, nullable=False)
    is_delivered = Column(Boolean, nullable=False)
    billet_sale_id = relationship("Billet", backref="Sale")
    invoice_sale_id = relationship("Invoice", backref="Sale")
    
    def __init__(self, client_id, salesman_id, item_list, sale_date, total, image_id, pay_type, pay_term, is_paid, is_delivered):
        self.client_id = client_id
        self.salesman_id = salesman_id
        self.item_list = item_list
        self.sale_date = sale_date
        self.total = total
        self.image_id = image_id
        self.pay_type = pay_type
        self.pay_term = pay_term
        self.is_paid = is_paid
        self.is_delivered = is_delivered

class Billet(Base):
    r'''
    Registro de boletos gerados na API da gerencianet
    :status
    1 - Pago
    2 - Em aberto
    '''
    __tablename__ = 'billet'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    sale_id = Column(Integer, ForeignKey(Sale.id, ondelete='SET NULL'))
    value = Column(Float, nullable=False)
    expire_date = Column(Date, nullable=False)
    status = Column(Integer, nullable=False)
    transaction_id = Column(String, nullable=False)
    barcode = Column(String)
    pixcode = Column(String)
    billet_link = Column(String)
    billet_pdf_link = Column(String)

    def __init__(self, sale_id, value, expire_date, status, transaction_id, barcode, pixcode, billet_link, billet_pdf_link):
        self.sale_id = sale_id
        self.value = value
        self.expire_date = expire_date
        self.status = status
        self.transaction_id = transaction_id
        self.barcode = barcode
        self.pixcode = pixcode
        self.billet_link = billet_link
        self.billet_pdf_link = billet_pdf_link

class Invoice(Base):
    __tablename__ = 'invoice'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    sale_id = Column(Integer, ForeignKey(Sale.id, ondelete='SET NULL'))
    value = Column(Float)
    invoice_datetime = Column(DateTime)
    uuid = Column(String)
    status = Column(String)
    nfe_number = Column(String)
    receipt = Column(String)
    access_key = Column(String)
    xml = Column(String)
    danfe = Column(String)

    def __init__(self, sale_id, value, invoice_datetime, uuid, status, nfe_number, receipt, access_key, xml, danfe):
        self.sale_id = sale_id
        self.value = value
        self.invoice_datetime = invoice_datetime
        self.uuid = uuid
        self.status = status
        self.nfe_number = nfe_number
        self.receipt = receipt
        self.access_key = access_key
        self.xml = xml
        self.danfe = danfe

class Error_Logs(Base):
    __tablename__ = 'error_logs'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    log = Column(String, nullable=False)
    log_datetime = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey(Person.id, ondelete='SET NULL'))
    service_id = Column(Integer, nullable=False)
    endpoint = Column(String, nullable=False)

    def __init__(self, log, log_datetime, user_id, service_id, endpoint):
        self.log = log
        self.log_datetime = log_datetime
        self.user_id = user_id
        self.service_id = service_id
        self.endpoint = endpoint

class Access(Base):
    __tablename__ = 'access'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    user_id = Column(Integer, ForeignKey(Person.id, ondelete='SET NULL'))
    access_datetime = Column(DateTime, nullable=False)
    endpoint = Column(String, nullable=False)

    def __init__(self, user_id, access_datetime, endpoint):
        self.user_id = user_id
        self.access_datetime = access_datetime
        self.endpoint = endpoint

class Permissions(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    p_name = Column(String, nullable=False)
    permission1 = Column(Boolean)
    permission2 = Column(Boolean)
    permission3 = Column(Boolean)
    permission4 = Column(Boolean)
    permission5 = Column(Boolean)
    permission6 = Column(Boolean)
    permission7 = Column(Boolean)

    def __init__(self, permission1, permission2, permission3, permission4, permission5, permission6, permission7):
        self.permission1 = permission1
        self.permission2 = permission2
        self.permission3 = permission3
        self.permission4 = permission4
        self.permission5 = permission5
        self.permission6 = permission6
        self.permission7 = permission7