import asyncio
import traceback
import typing
import uuid

from ... import words
from ...quru_logger import logger
from ...env import PPL_RPC_TIMEOUT, DEBUG
from .abs_types import BasableLayerABC, UpperLayerABC
from .layer1 import Layer1


'''
Layer 2 format
{
    "header": str
    "receipt_id": str
    "mode": str
    "source": str
    "payload": Packet
}
'''


class RPCTimeoutError(Exception):
    pass


class Layer2(BasableLayerABC, UpperLayerABC):
    '''Not only RPC'''
    layer_name = "layer2"

    class _PassToFlag:
        def __init__(self, *args):
            self.data = args

    def __init__(self, base_layer: Layer1):
        super().__init__()
        self._base_layer = base_layer
        self._base_layer.pile(self)
        self._routing_table = {}
        self._receipts = {}

    async def callback(self, packet: words.RPCPacket) -> bool:
        '''A callback function for handling received packet.
        '''
        if packet.mode == "receipt":
            self._wake_by_receipt(packet.receipt_id, packet.payload)
        else:
            try:
                receipt = await self._dispatch(packet)
            except (words.TransmittableException, RPCTimeoutError) as e:
                receipt = e
            except Exception as e:
                if DEBUG:
                    logger.error("Error!", error=traceback.format_exc())
                else:
                    logger.warning("Error!", error=str(e))
                receipt = words.TransmittableException(str(e))
            if isinstance(receipt, self._PassToFlag):
                routing_key, payload, inner_protl, props =\
                    receipt.data
                packet.payload = payload
                packet.inner_protl = inner_protl
                await self._base_layer.send(
                    routing_key,
                    packet,
                    self.layer_name,
                    props)
            elif receipt is None:
                # Keep silent
                pass
            elif packet.mode == "send":
                # This procedure wont to be returned.
                pass
            elif packet.mode == "call":
                # This procedure meant to be returned/forward.
                rp_packet = words.RPCPacket()
                rp_packet.mode = "receipt"
                rp_packet.payload = receipt
                rp_packet.source = self.name
                rp_packet.receipt_id = packet.receipt_id
                await self._base_layer.send(packet.source,
                                            rp_packet,
                                            self.layer_name,
                                            None)
            else:
                raise Exception("Unrecognized mode "
                                "{}!".format(self.layer_name))
        return False

    async def send(self, routing_key: str,
                   payload: typing.Any,
                   inner_protl: str,
                   props,
                   exg_name=None):
        packet = words.RPCPacket()
        packet.mode = "send"
        packet.payload = payload
        packet.source = self.name
        packet.inner_protl = inner_protl
        await self._base_layer.send(
            routing_key, packet,
            self.layer_name, props, exg_name)

    async def call(self, routing_key: str,
                   payload: typing.Any,
                   inner_protl: str,
                   props,
                   timeout=None,
                   exg_name=None):
        packet = words.RPCPacket()
        receipt_id = str(uuid.uuid4())
        packet.receipt_id = receipt_id
        packet.mode = "call"
        packet.payload = payload
        packet.source = self.name
        packet.inner_protl = inner_protl

        future = self._base_layer.loop.create_future()
        self._receipts[receipt_id] = future
        await self._base_layer.send(
            routing_key, packet,
            self.layer_name, props, exg_name)

        if PPL_RPC_TIMEOUT > 0:
            def raise_rpc_timeout_error(future: asyncio.Future):
                if not future.done():
                    future.set_result(
                        RPCTimeoutError(
                            "Receipt {} expired"
                            "".format(receipt_id)))
            self._base_layer.loop.call_later(
                timeout or (PPL_RPC_TIMEOUT * 0.001),
                raise_rpc_timeout_error,
                future)
        receipt = await future
        self._receipts.pop(receipt_id)
        if isinstance(receipt, words.TransmittableException):
            logger.warning(
                "Exception_occured_in_remote_rpc_calling.",
                routing_key=routing_key,
                receipt_id=receipt_id,
                error=str(receipt))
            raise receipt
        elif isinstance(receipt, RPCTimeoutError):
            logger.warning(
                "RPC_timeout_occured!",
                routing_key=routing_key,
                receipt_id=receipt_id)
            raise receipt
        return receipt

    def passto(self, routing_key: str,
               payload: typing.Any,
               inner_protl: str,
               props):
        return self._PassToFlag(routing_key, payload, inner_protl, props)

    def _wake_by_receipt(self, receipt_id: str, receipt: typing.Any):
        if receipt_id not in self._receipts:
            logger.info("Receipt_not_found", name=self.name)
            return
        future = self._receipts[receipt_id]
        if future.done():
            logger.warning(
                "RPC_receipt_invalid_due_to_late.",
                receipt_id=receipt_id)
            return
        future.set_result(receipt)
        return

    async def _setup(self):
        logger.info("Setting_up_layer2...", name=self.name)
