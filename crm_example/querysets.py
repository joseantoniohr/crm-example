from django.db import models


class SoftDeleteQuerySet(models.query.QuerySet):

    def delete(self):
        try:
            self.update(is_deleted=True)
        except Exception:
            # TODO: we should log this error with error monitoring tool
            pass
