import asyncio
from typing import Type

from tracardi_plugin_sdk.action_runner import ActionRunner


def run_plugin(plugin: Type[ActionRunner], init, payload):
    async def main(plugin, init, payload):
        try:

            build_method = getattr(plugin, "build", None)
            if build_method and callable(build_method):
                plugin = await build_method(**init)
            else:
                plugin = plugin(**init)

            return await plugin.run(payload)

        except Exception as e:
            if isinstance(plugin, ActionRunner):
                await plugin.on_error()
            raise e
        finally:
            if isinstance(plugin, ActionRunner):
                await plugin.close()

    asyncio.run(main(plugin, init, payload))
