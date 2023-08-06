from zpy.custom import Plugin
from zpy.api import ApiConfiguration
from zpy.cloud.aws.ssm import SSMParameter
from zpy.cloud.aws.firehose import Firehose
from zpy.db.oracle import OracleDB
import os


class PFirehose(Plugin):
    def initialize(self, config: ApiConfiguration, ssm: SSMParameter, **kwargs):
        return Firehose(with_profile=True)


class POracle(Plugin):
    """"""

    def initialize(self, config: ApiConfiguration, ssm: SSMParameter, **kwargs):

        local_client = None if "local_client" not in kwargs else kwargs["local_client"]
        verbose = False if "verbose" not in kwargs else kwargs["verbose"]
        schemas = None if "schemas" not in kwargs else kwargs["schemas"]
        pool_initialize = (
            False if "pool_initialize" not in kwargs else kwargs["pool_initialize"]
        )
        db = OracleDB(
            config=config.to_dict(),
            local_client_path=local_client,
            schemas=schemas,
            env=config.ENVIRONMENT,
            verbose=verbose,
        )
        if pool_initialize:
            try:
                if config.ENVIRONMENT == "localdev":
                    db.init_local_client(os.getenv("LOCAL_CLIENT"))
                db.initialize_pool(
                    dns=db.get_tsn_dsn_conenction(config.to_dict(), "DSN"),
                    homogeneous=True,
                    user=config.DB_USER,
                    pwd=config.DB_PASSWORD,
                )
            except Exception as e:
                print(e)
        return db