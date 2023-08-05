from .protocol import Layer1, Layer2, Layer3, Layer4Actor


class NodeServer(Layer4Actor):
    def __init__(self,
                 role=None,
                 name=None,
                 priority_queue=False,
                 prefetch=10,
                 loop=None,
                 test_mode=False):
        base_layer = Layer3(
            Layer2(
                Layer1(name=name, loop=loop, test_mode=test_mode)
            )
        )
        super().__init__(role=role, base_layer=base_layer,
                         prefetch_counter=prefetch,
                         priority_queue=priority_queue)

    def run(self):
        self._base_layer._base_layer._base_layer.run()

    async def setup(self):
        await self._base_layer._base_layer._base_layer._real_setup()
