from src import db
from src.models.model_base import ModelBase


class PostgersSyncLogModel(ModelBase):
    __tablename__ = 'postgres_sync_logs'
    global_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    last_sync_id_to_envizi = db.Column(db.Integer(), nullable=False, default=0)
    last_sync_datetime_to_envizi = db.Column(db.DateTime())

    @classmethod
    def find_by_global_uuid(cls, global_uuid: str):
        return cls.query.filter_by(global_uuid=global_uuid).first()

    def update_sync_log(self):
        log = self.query.filter_by(global_uuid=self.global_uuid).first()
        if log:
            log.update(**{
                'last_sync_id_to_envizi': self.last_sync_id_to_envizi,
                'last_sync_datetime_to_envizi': self.last_sync_datetime_to_envizi
            })
        else:
            self.save_to_db()

    @classmethod
    def get_last_sync_id_to_envizi(cls, global_uuid: str) -> int:
        log = cls.query.filter_by(global_uuid=global_uuid).first()
        if log:
            return log.last_sync_id_to_envizi
        return 0
