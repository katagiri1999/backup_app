import dataclasses

from chalicelib.common_modules.const import const


@dataclasses.dataclass
class Team:
    team_id: str = None
    team_name: str = None

    def to_dict(self):
        try:
            return dataclasses.asdict(self)

        except Exception as e:
            raise e

    def validation(self):
        try:
            errors = []

            if not self.team_id:
                errors.append(const.team_id)
            if not self.team_name:
                errors.append(const.team_name)

            if len(errors) > 0:
                err_params = {
                    const.exception: "invalid " + ", ".join(errors),
                    const.status_code: 400,
                }
                raise Exception(err_params)

        except Exception as e:
            raise e
