class ActionRunner:
    id = None
    debug = False
    event = None
    session = None
    profile = None
    flow = None
    flow_history = None
    console = None

    async def run(self, **kwargs):
        pass

    async def close(self):
        pass
