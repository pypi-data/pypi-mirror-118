from event_stream.models.model import *
from sqlalchemy import Table, Column, MetaData, create_engine
import os
import urllib
from sqlalchemy.orm import sessionmaker


class DAO(object):

    def __init__(self):
        host_server = os.environ.get('POSTGRES_HOST', 'postgres')
        db_server_port = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_PORT', '5432')))
        database_name = os.environ.get('POSTGRES_DB', 'amba')
        db_username = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_USER', 'streams')))
        db_password = urllib.parse.quote_plus(str(os.environ.get('POSTGRES_PASSWORD', 'REPLACE_ME')))

        # ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
        DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(db_username, db_password, host_server,
                                                            db_server_port, database_name)
        print(DATABASE_URL)
        engine = create_engine('postgresql+psycopg2://streams:REPLACE_ME@postgres:5432/amba')
        Base.metadata.create_all(engine)
        # database = databases.Database(DATABASE_URL)

        Session = sessionmaker(bind=engine)
        self.session = Session()

    def save_object(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_object(self, table, key):
        return self.session.query(table).get(key)

    def save_if_not_exist(self, obj, table, key):
        obj_db = self.get_object(table, key)
        if not obj_db:
            return self.save_object(obj)
        else:
            return obj_db

    def save_publication(self, publication_data):
        publication = Publication.objects(doi=publication_data['doi'], type=publication_data['type'],
                                          pubDate=publication_data['pubDate'], year=publication_data['year'],
                                          publisher=publication_data['publisher'],
                                          citationCount=publication_data['citationCount'],
                                          title=publication_data['title'],
                                          normalizedTitle=publication_data['normalizedTitle'],
                                          abstract=publication_data['abstract'])
        publication = self.save_object(publication)

        authors = publication_data['authors']
        for author_data in authors:
            author = Author(name=author_data['name'],  normalizedName=author_data['normalizedName'])
            author = self.save_if_not_exist(author, Author, {'normalizedName': author.normalized_name})

            publication_authors = PublicationAuthor({'authorId': author.id, 'publicationId': publication.id})
            self.save_object(publication_authors)

        sources = publication_data['source_id']
        for sources_data in sources:
            source = Source(title=sources_data['title'],  url=sources_data['url'])
            source = self.save_if_not_exist(source, Source, {'title': source.title})
            publication_sources = PublicationSource({'sourceId': source.id, 'publicationId': publication.id})
            self.save_object(publication_sources)

        fields_of_study = publication_data['fieldOfStudy']
        for fos_data in fields_of_study:
            fos = FieldOfStudy(name=fos_data['name'],  normalizedName=fos_data['normalizedName'])
            fos.level = 2
            fos = self.save_if_not_exist(fos, FieldOfStudy, {'normalizedName': fos.normalized_name})
            publication_fos = PublicationFieldOfStudy({'fieldOfStudyId': fos.id, 'publicationId': publication.id})
            self.save_object(publication_fos)

        return publication
        # todo
        # publicationCitations = PublicationCitations()
        # publicationReferences = PublicationReferences(**author_data)
