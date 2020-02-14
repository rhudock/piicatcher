from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
# forensic functions
import hashlib
# file format converters
from tika import parser
# process control
from multiprocessing import Pool
# gui
from easygui import diropenbox, fileopenbox
# filesystem related libraries
from pathlib import Path
import itertools
from unidecode import unidecode
from datetime import datetime
import mimetypes
import uuid
import re

# PHI Scanner
# from .explorer.files import dispatch

Base = declarative_base()
# TODO Need to split files over 10000 lines else crash NLP split -l 10000 929aae55-e921-4279-849c-980331858df0.txt
#  929aae55-e921-4279-849c-980331858df0
# TODO filter on .txt, need to rename split files to remove excess entry
#  find . -name '*\.a*' | while read f; do mv "$f" "${f//\.a/}"; done



def main():
    file = Path("db.sqlite")
    if file.exists():
        print("File exists")
        exit(1)
    else:
        print("File not exist")
        output_dir = "/Users/rhudock/output/"
        mimetypes.init()
        db_uri = 'sqlite:///db.sqlite'  # https://www.sqlite.org/datatype3.html
        engine = create_engine(db_uri)
        _session = sessionmaker(bind=engine)
        session = _session()
        # Files.__table__.create(engine)
        Base.metadata.create_all(engine)
        dir_to_open = diropenbox(msg="select directory:")
        path_list = Path(dir_to_open).glob('**/*.msg')
        for path in path_list:
            # because path is object not string
            path_in_str = str(path)
            print(path_in_str)
            # parsed = parser.from_file(path_in_str, 'http://127.0.0.1:'+str(PORT)+'/tika')
            md5 = md5_checksum(path_in_str)
            name = path.name
            file_format_type = file_type(path.suffix)
            (content, meta) = tika_parser(path_in_str)
            file_length = len(content)
            unique_ref = uuid.uuid4()
            output_file = str(output_dir) + str(unique_ref) + ".txt"
            f = open(output_file, "w+")
            f.writelines(content)
            f.close()
            new_file = Files(Name=name, Path=path_in_str, FileRef=output_file, MetaRef=str(unique_ref),
                             MD5=md5, FileType=file_format_type, FileLength=file_length)
            session.add(new_file)
            session.commit()
            for x in meta.keys():
                new_file = MetaData(FileRef=str(unique_ref), Key=str(x), KeyValue=str(meta[x]))
                session.add(new_file)
                session.commit()
        from prettytable import from_db_cursor
        import sqlite3 as lite
        con = lite.connect('db.sqlite')
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Files;')
            x = from_db_cursor(cur)
            # print(str(df))
        print(x)
        # pool = Pool()
        # pool.map(tika_parser, paths)


class Files(Base):
    __tablename__ = 'Files'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Path = Column(String)
    FileRef = Column(String)
    MetaRef = Column(String)
    MD5 = Column(String)
    FileLength = Column(Integer)
    FileType = Column(String)

    @property
    def __repr__(self):
        return f"File: {self.Id, self.Name, self.MD5, self.FileType, self.FileRef, self.MetaRef, self.FileLength}"


class MetaData(Base):
    __tablename__ = 'Metadata'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    FileRef = Column(String)
    Key = Column(String)
    KeyValue = Column(String)

    @property
    def __repr__(self):
        return f"File: {self.Id, self.FileRef, self.Key, self.KeyValue}"


def md5_checksum(file_path):
    with open(file_path, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def clean_text(text_to_clean):
    return ''.join(c for c in text_to_clean if c.isprintable())


def file_type(file_extension):
    mimetypes.add_type('application/vnd.ms-outlook',
                       '.msg',
                       True
                       )
    return mimetypes.types_map[file_extension]


def tika_parser(file_path):
    """Returns converted format"""
    port = 32768
    # Extract text from document
    content = parser.from_file(file_path, 'http://127.0.0.1:' + str(port) + '/tika')
    if 'content' in content:
        text = content['content']
        meta = content['metadata']
    else:
        return
    # assert isinstance(meta, object)
    text = re.sub(r'(\n){2,}', '\n', str(text))
    return str(text), meta


if __name__ == '__main__':
    main()
