from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, exists, asc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# region Table
class Zdaniye(Base):
    __tablename__ = 'zdaniye'

    id = Column(Integer, primary_key=True, autoincrement=True)
    zname = Column(String)
    descr = Column(String)
# endregion

class Auditoriya(Base):
    __tablename__ = 'auditoriya'

    id = Column(Integer, primary_key=True, autoincrement=True)
    z_id = Column(Integer)
    aname = Column(String)
    etaj = Column(Integer)
    descr = Column(String)
    ipcam = Column(String)
    do_surv = Column(Integer)

class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///Database/mydb.db', echo=False)
        self.conn = self.engine.connect()
        #metadata = MetaData()
        #self.Zdaniye = Table('zdaniye', metadata, autoload=True, autoload_with=self.engine)

    def __del__(self):
        self.con.close()

    def selectAllZdaniye(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Zdaniye).all()
        #for row in result:
        #    print("ZName: ", row.zname, "Descr:", row.descr)
        return result

    def insertZdaniye(self, zname, descr):
        Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        session = Session()
        c1 = Zdaniye(zname = zname, descr = descr)
        session.add(c1)
        session.flush()
        session.commit()
        session.close()

    def deleteZdaniye(self, id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        x = session.query(Zdaniye).get(id)
        print(x)
        session.delete(x)
        session.commit()

    def updateZdaniye(self, id, colIndex, value):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        b = False
        if session.query(exists().where(Zdaniye.id==id)).scalar():
            if colIndex==1:
                colName = 'zname'
            elif colIndex==2:
                colName = 'descr'
            session.query(Zdaniye).filter_by(id=id).update({colName : value})
            b = True
        session.commit()
        return b

    def selectAllAuditoriya(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Auditoriya).all()
        return result

    def selectAuditoriyaByZ_Id(self, z_id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Auditoriya).filter_by(z_id=z_id).all()
        return result

    def selectAuditoriyaByZ_Id_and_Etaj(self, z_id, etaj):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        result = session.query(Auditoriya).filter_by(z_id=z_id, etaj=etaj).all()
        return result

    def insertAuditoriya(self, z_id, aname, etaj, descr, ipcam, do_surv):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        aRow = Auditoriya(z_id=z_id, aname = aname, etaj = etaj, descr=descr, ipcam = ipcam, do_surv = do_surv)
        session.add(aRow)
        session.commit()

    def deleteAuditoriya(self, id):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        x = session.query(Auditoriya).get(id)
        print(x)
        session.delete(x)
        session.commit()

    def updateAuditoriya(self, id, colIndex, value):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        b = False
        if session.query(exists().where(Auditoriya.id==id)).scalar():
            if colIndex==2:
                colName = 'aname'
            elif colIndex==3:
                colName = 'etaj'
            elif colIndex==4:
                colName = 'descr'
            elif colIndex==5:
                colName = 'ipcam'
            elif colIndex==6:
                colName = 'do_surv'
            session.query(Auditoriya).filter_by(id=id).update({colName : value})
            b = True
        session.commit()
        return b


