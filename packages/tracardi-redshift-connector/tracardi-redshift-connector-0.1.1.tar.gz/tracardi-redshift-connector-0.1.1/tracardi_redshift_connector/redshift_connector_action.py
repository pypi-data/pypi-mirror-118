from typing import Optional

from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.result import Result

from tracardi_redshift_connector.plugin.redshift_connector import redshift_conn


class RedshiftConnectorAction(ActionRunner):

    def __init__(self, **kwargs):
        self.database = kwargs['dbname'] if 'dbname' in kwargs else None
        self.user = kwargs['user'] if 'database' in kwargs else None
        self.password = kwargs['password'] if 'database' in kwargs else None
        self.port = kwargs['port'] if 'port' in kwargs else '5439'

    async def run(self, query):
        result = await (redshift_conn(self.database, self.user, self.password, self.port), query)
        return Result(port="payload", value=result)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_redshift_connector.redshift_connector_action',
            className='RedshiftConnectorAction',
            inputs=["query"],
            outputs=['payload'],
            version='0.1.4',
            license="MIT",
            author="Bartosz Dobrosielski",
            init={
                "source": {
                    "id": None,
                },
                "redshift": {
                    "database": None,
                    "host": None,
                    "user": None,
                    "password": None,
                    "collection": None
                }
            }

        ),
        metadata=MetaData(
            name='Redshift connector',
            desc='Connects to redshift and reads data.',
            type='flowNode',
            width=200,
            height=100,
            icon='redshift',
            group=["Connectors"]
        )
    )