from red_warden.mvc import RWValidationModelBase
from red_warden.enums import RWYesNoEnum
from red_warden.datalayer import RWDataLayer
from red_warden.datazones.RWManager.models import RWKeyModel


class RWSessionLogic:
    @classmethod
    async def authenticate(cls, **kwargs):
        class ValidationModel(RWValidationModelBase):
            username: str
            password: str

        data = ValidationModel(**kwargs).dict()

        row = await RWDataLayer.load_one(
            RWKeyModel, filters=["login:eq:%s" % data["username"]]
        )
        if not row or not RWKeyModel.check_password(
            row["password_hash"], data["password"]
        ):
            return False

        return row

    @classmethod
    async def toggle_mfa(cls, **kwargs):
        class ValidationModel(RWValidationModelBase):
            key_id: str
            status: RWYesNoEnum

        data = ValidationModel(**kwargs).dict()

        row = await RWDataLayer.load_by_id(RWKeyModel, data["key_id"], None)
        if not row:
            return None

        return await RWDataLayer.save(
            RWKeyModel,
            data["key_id"],
            RWKeyModel.toggle_mfa(row["mfa_enabled"], data["status"]),
            None,
            True,
        )

    @classmethod
    async def check_otp(cls, **kwargs):
        class ValidationModel(RWValidationModelBase):
            key_id: str
            otp_code: str

        data = ValidationModel(**kwargs).dict()

        row = await RWDataLayer.load_by_id(RWKeyModel, data["key_id"], None)
        if not row:
            return None

        if not RWKeyModel.check_otp(row["mfa_secret"], data["otp_code"]):
            return False

        return row

    @classmethod
    async def login(cls, logged_in_key):
        # generic scope used when a function needs a user but not a specific scope
        scope = ["logged_in"]

        return {"key_id": logged_in_key["id"], "scope": scope}
