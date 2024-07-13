import dataclasses

from chalicelib.common_modules.const import const


@dataclasses.dataclass
class User:
    user_id: str = None
    team_id: str = None
    role: str = None

    def to_dict(self):
        try:
            return dataclasses.asdict(self)

        except Exception as e:
            raise e

    def validation(self):
        try:
            errors = []

            if not self.user_id:
                errors.append(const.user_id)
            if not self.team_id:
                errors.append(const.team_id)
            if not self.role:
                errors.append(const.role)

            if self.role:
                if self.status not in [const.admin, const.normal]:
                    errors.append("role format")

            if len(errors) > 0:
                err_params = {
                    const.exception: "invalid " + ", ".join(errors),
                    const.status_code: 400,
                }
                raise Exception(err_params)

        except Exception as e:
            raise e
