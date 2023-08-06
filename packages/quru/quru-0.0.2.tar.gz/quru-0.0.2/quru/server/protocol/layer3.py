import typing

import aiozipkin as az

from ... import words
from ...quru_logger import logger
from ...env import DEBUG, SPAN_SAMPLE_RATE, ZIPKIN_ADDR
from .abs_types import BasableLayerABC, UpperLayerABC
from .layer2 import Layer2


class Layer3(BasableLayerABC, UpperLayerABC):
    layer_name = "layer3"

    def __init__(self, base_layer: Layer2):
        super().__init__()
        self._base_layer = base_layer
        self._base_layer.pile(self)

    async def callback(self, packet: words.TracedPacket):
        if packet.trace_context is not None:
            span = self._tracer.join_span(packet.trace_context)
            with span as span:
                rtn_v = await self._dispatch(packet, span)
        else:
            span, _ = self._create_trace()
            rtn_v = await self._dispatch(packet, span)
        return rtn_v

    async def send(
        self,
        routing_key: str,
        payload: typing.Any,
        inner_protl: str,
        props,
        span: az.span.SpanAbc = None,
        exg_name=None
    ):
        headless = False
        if span is None:
            headless = True
            span, trace = self._create_trace()
            trace.start()
            span.start()
        packet = words.TracedPacket()
        packet.trace_context = self._tracer.new_child(span.context).context
        packet.payload = payload
        packet.inner_protl = inner_protl
        await self._base_layer.send(
            routing_key,
            packet,
            self.layer_name,
            props,
            exg_name=exg_name)
        if headless:
            span.finish()
            trace.finish()

    async def call(
        self,
        routing_key: str,
        payload: typing.Any,
        inner_protl: str,
        props,
        span: az.span.SpanAbc = None,
        timeout=None,
        exg_name=None
    ):
        headless = False
        if span is None:
            headless = True
            span, trace = self._create_trace()
            trace.start()
            span.start()
        packet = words.TracedPacket()
        packet.trace_context = self._tracer.new_child(span.context).context
        packet.payload = payload
        packet.inner_protl = inner_protl
        tmp = await self._base_layer.call(
            routing_key,
            packet,
            inner_protl=self.layer_name,
            props=props,
            timeout=timeout,
            exg_name=exg_name)
        if headless:
            span.finish()
            trace.finish()
        return tmp

    def passto(
        self,
        routing_key: str,
        payload: typing.Any,
        inner_protl: str,
        props,
        span: az.span.SpanAbc = None
    ):
        headless = False
        if span is None:
            headless = True
            span, trace = self._create_trace()
            trace.start()
            span.start()
        packet = words.TracedPacket()
        packet.trace_context = self._tracer.new_child(span.context).context
        packet.payload = payload
        packet.inner_protl = inner_protl
        if headless:
            span.finish()
            trace.finish()
        return self._base_layer.passto(
            routing_key,
            packet,
            self.layer_name,
            props)

    def _create_trace(self, name="", span_name="")\
            -> typing.Tuple[az.span.SpanAbc, az.span.SpanAbc]:
        trace = self._tracer.new_trace(
            sampled=(name != ""), debug=DEBUG)
        trace.name(name)
        # trace.kind(az.CLIENT)
        span = self._tracer.new_child(trace.context)
        span.name(span_name)
        # span.kind(az.CLIENT)
        return span, trace

    async def _setup(self):
        logger.info("Setting_up_layer3...", name=self.name)
        endpoint = az.create_endpoint(service_name=self.name[:20])
        self._tracer = await az.create(
            ZIPKIN_ADDR,
            endpoint,
            sample_rate=SPAN_SAMPLE_RATE)
        logger.info("Succeded_in_connecting_zipkin.", address=ZIPKIN_ADDR,
                    sample=SPAN_SAMPLE_RATE)

    async def _teardown(self):
        logger.info("Tearing_down_layer3...", name=self.name)
        await self._tracer.close()
