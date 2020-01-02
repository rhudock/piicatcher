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
# PHI Scanner
from .explorer.files import dispatch


Base = declarative_base()


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
        path_list = Path(dir_to_open).glob('**/*.docx')
        for path in path_list:
            # because path is object not string
            path_in_str = str(path)
            print(path_in_str)
            # parsed = parser.from_file(path_in_str, 'http://127.0.0.1:'+str(PORT)+'/tika')
            md5 = md5_checksum(path_in_str)
            name = path.name
            file_format_type = fileType(path.suffix)
            content = tika_parser(path_in_str)
            file_length = len(content)
            unique_ref = uuid.uuid4()
            output_file = str(output_dir) + str(unique_ref) + ".txt"
            f = open(output_file, "w+")
            f.writelines(content)
            f.close()
            new_file = Files(Name=name, Path=path_in_str, FileRef=output_file, MD5=md5,
                             FileType=file_format_type, FileLength=file_length)
            session.add(new_file)
            session.commit()
        query = session.query(Files).all()
        df = pd.DataFrame(query)
        df.head(4)
        # print(str(df))
        # pool = Pool()
        # pool.map(tika_parser, paths)


class Files(Base):
    __tablename__ = 'Files'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String)
    Path = Column(String)
    FileRef = Column(String)
    MD5 = Column(String)
    FileLength = Column(Integer)
    FileType = Column(String)

    @property
    def __repr__(self):
        return f"File: {self.Id, self.Name, self.MD5, self.FileType, self.FileRef, self.FileLength}"


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


def fileType(file_extension):
    return mimetypes.types_map[file_extension]


def tika_parser(file_path):
    """Returns converted format"""
    port = 32768
    # Extract text from document
    content = parser.from_file(file_path, 'http://127.0.0.1:' + str(port) + '/tika')
    if 'content' in content:
        text = content['content']
    else:
        return
    # Convert to string
    return clean_text(str(text))


if __name__ == '__main__':
    main()
