from src import db
from src.models.model_base import ModelBase


class PostgersSyncLogModel(ModelBase):
    __tablename__ = 'postgres_sync_logs'
    global_uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    last_sync_id = db.Column(db.Integer(), nullable=False, default=0)

    def update_last_sync_id(self):
        log = self.query.filter_by(global_uuid=self.global_uuid).first()
        if log:
            log.update(**{'last_sync_id': self.last_sync_id})
        else:
            self.save_to_db()

    @classmethod
    def get_last_sync_id(cls, global_uuid: str):
        log = cls.query.filter_by(global_uuid=global_uuid).first()
        if log:
            return log.last_sync_id
        return 0


