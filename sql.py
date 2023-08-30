from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Audio(Base):
    __tablename__ = 'audio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    words = relationship('Word', back_populates='audio')
    dictations = relationship('Dictation', back_populates='audio')


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    audio_id = Column(Integer, ForeignKey('audio.id'), nullable=False)
    word = Column(String, nullable=False)
    word_start_time = Column(Integer, nullable=False)
    word_end_time = Column(Integer, nullable=False)
    audio = relationship('Audio', back_populates='words')


class Dictation(Base):
    __tablename__ = 'dictation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dictation_time = Column(String, nullable=False)
    error_word = Column(String)
    audio_id = Column(Integer, ForeignKey('audio.id'))
    audio = relationship('Audio', back_populates='dictations')


class DictationSql:
    def __init__(self):
        self.engine = create_engine('sqlite:///dictation.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def set_dictation_audio(self, name, location, word_size, words):
        try:
            with self.session.begin():
                audio = Audio(name=name, location=location, word_count=word_size)
                self.session.add(audio)
            word_entries = [Word(audio_id=audio.id, word=word, word_start_time=start_time, word_end_time=end_time)
                            for word, start_time, end_time in words]
            with self.session.begin():
                self.session.add_all(word_entries)
        except Exception as e:
            print("Error:", e)

    def get_audio_with_word(self, index=None):
        try:
            words = self.session.query(Word.word).filter_by(audio_id=audio_index).all()
            return [word[0] for word in words]
        except Exception as e:
            print("Error:", e)

    def set_dictation(self, dictation_time, error_word, audio_id):
        try:
            with self.session.begin():
                dictation_entry = Dictation(dictation_time=dictation_time, error_word=error_word, audio_id=audio_id)
                self.session.add(dictation_entry)
        except Exception as e:
            print("Error:", e)

    def get_words_by_audio_index(self, audio_name: str):
        try:
            if audio_name:
                audio = self.session.query(Audio).filter(Audio.name == audio_name).all()
            else:
                audio = self.session.query(Audio).all()
            return audio
        except Exception as e:
            print("Error:", e)

    def get_error_words_by_audio_and_time(self, audio_index, start_time, end_time):
        try:
            error_words = (
                self.session.query(Dictation.error_word)
                .join(Audio)
                .filter(Audio.id == audio_index)
                .filter(Dictation.dictation_time.between(start_time, end_time))
                .all()
            )
            return [word[0] for word in error_words]
        except Exception as e:
            print("Error:", e)

    def close(self):
        self.session.close()


if __name__ == '__main__':
    a = DictationSql()
    a.set_dictation_audio("Sample Audio", "/path/to/audio", 100, [("word1", 0, 1), ("word2", 2, 3)])
    a.close()
