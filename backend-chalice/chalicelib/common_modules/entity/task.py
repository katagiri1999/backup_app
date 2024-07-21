import dataclasses

from chalicelib.common_modules.const import const


@dataclasses.dataclass
class Task:
    task_id: str = None
    user_id: str = None
    team_id: str = None
    task: str = None
    detail: str = None
    status: str = None
    limit: str = None

    def to_dict(self):
        try:
            return dataclasses.asdict(self)

        except Exception as e:
            raise e

    def validation(self):
        try:
            errors = []

            if not self.task_id:
                errors.append(const.task_id)
            if not self.user_id:
                errors.append(const.user_id)
            if not self.team_id:
                errors.append(const.team_id)
            if not self.task:
                errors.append(const.task)
            if not self.status:
                errors.append(const.status)
            if not self.limit:
                errors.append(const.limit)

            if self.status:
                if self.status not in [const.Finished, const.Untouched, const.Processing]:
                    errors.append("status format")

            if len(errors) > 0:
                err_params = {
                    const.exception: "invalid " + ", ".join(errors),
                    const.status_code: 400,
                }
                raise Exception(err_params)

        except Exception as e:
            raise e
