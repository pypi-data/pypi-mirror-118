import os
import graphene
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidKey
from red_warden.graphql import RWGraphQLYesNoField
from red_warden.datazones.RWManager import KeyModel
from red_warden.datazones.graphql.key.types import Key


class CreateKey(graphene.ClientIDMutation):
    key = graphene.Field(Key, required=True)
    mfa_secret = graphene.String()

    class Input:
        login = graphene.String(required=True)
        password = graphene.String(required=True)
        enabled = RWGraphQLYesNoField(required=True)
        mfa_enabled = RWGraphQLYesNoField()

    @classmethod
    async def mutate_and_get_payload(cls, root, info, **kwargs):
        db = KeyModel.get_datazone_db(info)

        async with db.transaction() as tx:
            kwargs["id"] = await db.get_uuid()

            password = kwargs.pop("password", None)
            if password:
                salt = os.urandom(32)
                kdf = Scrypt(
                    salt=salt, length=32, n=2 ** 14, r=8, p=1, backend=default_backend()
                )
                b = kdf.derive(password.encode())
                kwargs["password_hash"] = "%s.%s" % (salt.hex(), b.hex())

            if kwargs["mfa_enabled"] == "Y":
                kwargs["mfa_secret"] = Fernet.generate_key()

            mfa_secret = kwargs.get("mfa_secret", None)

            await db.execute(KeyModel.insert().values(kwargs))

            kwargs.pop("password_hash", None)
            kwargs.pop("mfa_secret", None)
            return cls(key=Key(**kwargs), mfa_secret=mfa_secret.decode())


class CheckPassword(graphene.ClientIDMutation):
    key = graphene.Field(Key, required=True)

    class Input:
        login = graphene.String(required=True)
        password = graphene.String(required=True)

    @classmethod
    async def mutate_and_get_payload(cls, root, info, **kwargs):
        db = KeyModel.get_datazone_db(info)

        async with db.transaction():
            try:
                k = await db.fetch_one(
                    KeyModel.select().where(KeyModel.c.login == kwargs["login"])
                )

                salt, key = k.password_hash.split(".")
                kdf = Scrypt(
                    salt=bytes.fromhex(salt),
                    length=32,
                    n=2 ** 14,
                    r=8,
                    p=1,
                    backend=default_backend(),
                )
                kdf.verify(kwargs["password"].encode(), bytes.fromhex(key))

                key = Key.get_node(info, k.id)

            except InvalidKey:
                raise Exception("Invalid credentials")

        return cls(key=key)
