from marshmallow.fields import String
from marshmallow_objects.models import NestedModel
from zpy.api.models import ZModel

# Models 🚟


class DBSSMCredentialsModel(ZModel):
    uri = String(data_key="uri")
    port = String(data_key="port")
    service = String(data_key="service")
    user = String(data_key="user")
    password = String(data_key="pass")


class AESSSMModel(ZModel):
    aes_sk = String(data_key="aes_sk")


class AWSFirehoseModel(ZModel):
    access_key = String(data_key="access_key")
    secret_key = String(data_key="secret_key")


class AWSModel(ZModel):
    firehose = NestedModel(nested=AWSFirehoseModel)


class SSMConstants(ZModel):
    smm_prefix = String()
    local_db_ssm = String()
    db_smm = String()
    aes_sk = String()
    aws_ssm = String()
