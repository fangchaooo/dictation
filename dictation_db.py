from pprint import pprint

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

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
    audio_name = Column(String, ForeignKey('audio.name'), nullable=False)
    word = Column(String, nullable=False)
    word_chinese_mean = Column(String, nullable=False)
    word_start_time = Column(Integer, nullable=False)
    word_end_time = Column(Integer, nullable=False)
    audio = relationship('Audio', back_populates='words')


class Dictation(Base):
    __tablename__ = 'dictation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    dictation_time = Column(DateTime, nullable=False)
    error_word = Column(String)
    audio_name = Column(String, ForeignKey('audio.name'))
    audio = relationship('Audio', back_populates='dictations')


class DictationDB:
    def __init__(self):
        self.engine = create_engine('sqlite:///dictation.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get_audio_and_wordinfo_for_tree_view(self):
        audio_dictations = self.session.query(Audio, Dictation).outerjoin(Dictation,
                                                                     Audio.name == Dictation.audio_name).all()
        return audio_dictations



        # data_dict = {}
        # for audio, dictation in audio_dictations:
        #     if audio.name not in data_dict:
        #         data_dict[audio.name] = CustomItem(audio.name, self.root_item)
        #     dictation_text = f"{dictation.dictation_time} (ERROR: {len(dictation.error_word.split())})"
        #     data_dict[audio.name].children.append(CustomItem(dictation_text, data_dict[audio.name]))
        #

    def set_dictation_audio(self, name, location, word_size, words):
        try:
            with self.session.begin():
                audio = Audio(name=name, location=location, word_count=word_size)
                self.session.add(audio)
                word_entries = [
                    Word(audio_name=audio.name, word=word, word_chinese_mean=mean, word_start_time=start_time,
                         word_end_time=end_time)
                    for word, mean, start_time, end_time in words]
                self.session.add_all(word_entries)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print("Error:", e)

    def get_audio_with_word(self, index=None):
        try:
            words = self.session.query(Word.word).filter_by(audio_id=index).all()
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


if __name__ == "__main__":
    db = DictationDB()
    db.get_audio_and_wordinfo_for_tree_view()
