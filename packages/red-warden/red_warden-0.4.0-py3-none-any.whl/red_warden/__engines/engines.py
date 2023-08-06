import asyncio
import uuid
import base64
import json
from abc import ABC
from aioredis import ConnectionForcedCloseError, ConnectionClosedError
from red_warden.config import RWConfig, Backends, Logger


class RWEngine(ABC):
    _shutdown_event = asyncio.Event()

    async def run(self, *args, **kwargs):
        raise NotImplementedError

    async def stop(self):
        self._shutdown_event.set()


class RWRedisRpcEngine(RWEngine):
    _redis_rpc = None
    _redis_pubsub = None

    def __init__(self, redis_backend_name):
        self._redis_backend_name = redis_backend_name
        self._rpc_key = "%s:rpc" % RWConfig["RW_APP_NAME"].lower()
        self._pubsub_key = "%s:pubsub" % RWConfig["RW_APP_NAME"].lower()

    async def _rpc_listener(self):
        while not self._shutdown_event.is_set():
            try:
                self._redis_rpc = Backends.create_instance(self._redis_backend_name)
                await self._redis_rpc.connect()

                while not self._shutdown_event.is_set():
                    _, value = await self._redis_rpc.blpop(
                        "%s:requests" % self._rpc_key
                    )
                    data = json.loads(base64.b64decode(value).decode())

                    if data["rpc_name"] not in ["run", "stop", "execute"]:
                        rpc = getattr(self, data["rpc_name"], None)
                        if rpc:
                            resp = rpc(*data["args"], **data["kwargs"])
                            value = base64.b64encode(json.dumps(resp).encode())
                            resp_key = "%s:responses:%s" % (
                                self._rpc_key,
                                data["token"],
                            )
                            await self._redis_rpc.lpush(resp_key, value)
                            await self._redis_rpc.expire(resp_key, 10)

            except (
                ConnectionForcedCloseError,
                ConnectionClosedError,
                ConnectionRefusedError,
            ):
                if not self._shutdown_event.is_set():
                    Logger.info("Reconnecting RPC listener to Redis backend...")
                    await asyncio.sleep(0.5)

    async def _pubsub_listener(self):
        while not self._shutdown_event.is_set():
            try:
                self._redis_pubsub = Backends.create_instance(self._redis_backend_name)
                await self._redis_pubsub.connect()

                for ch in await self._redis_pubsub.subscribe(self._pubsub_key):
                    async for message in ch.iter():
                        print("TODO! Got message:", message)
            except (
                ConnectionForcedCloseError,
                ConnectionClosedError,
                ConnectionRefusedError,
            ):
                if not self._shutdown_event.is_set():
                    Logger.info("Reconnecting PubSub listener to Redis backend...")
                    await asyncio.sleep(0.5)

    async def run(self, *args, **kwargs):
        t1 = asyncio.create_task(self._rpc_listener())
        t2 = asyncio.create_task(self._pubsub_listener())
        await asyncio.gather(*[t1, t2])

    async def stop(self):
        await super().stop()
        if self._redis_rpc:
            await self._redis_rpc.disconnect()
        if self._redis_pubsub:
            await self._redis_pubsub.disconnect()

    async def execute(self, rpc_name, *args, **kwargs):
        rc = Backends.create_instance(self._redis_backend_name)
        await rc.connect()

        token = str(uuid.uuid4)
        req = {
            "token": token,
            "rpc_name": rpc_name,
            "args": args,
            "kwargs": kwargs,
        }
        data = base64.b64encode(json.dumps(req).encode())
        req_key = "%s:requests" % self._rpc_key
        await rc.lpush(req_key, data)
        await rc.expire(req_key, 10)

        resp = await rc.blpop("%s:responses:%s" % (self._rpc_key, token), timeout=5)
        if not resp:
            raise Exception("Redis request timed out")
        data = json.loads(base64.b64decode(resp[1]).decode())
        await rc.disconnect()
        _redis_client = None
        return data


"""
from red_warden.helpers import get_random_element, CustomJsonEncoder
import traceback
import functools
import pika
import json
from pika.adapters.asyncio_connection import AsyncioConnection

class _AmqpAsyncConsumer:
    ""This is an example consumer that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, this class will stop and indicate
    that reconnection is necessary. You should look at the output, as
    there are limited reasons why the connection may be closed, which
    usually are tied to permission related issues or socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    ""

    EXCHANGE = "red_warden_rpc"

    def __init__(self):
        ""Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.
        ""
        self.was_consuming = False

        self._connection = None
        self._channel = None
        self._closing = False
        self._close_event = asyncio.Event()

        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1
        self.queue_routes = []

    async def run(self):
        LOGGER.info("Connecting to RabbitMQ...")
        self._connection = AsyncioConnection(
            parameters=pika.URLParameters(
                url=get_random_element(Config["RW_AMQP_BROKER_HOST"])
            ),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

        await self._close_event.wait()

    def on_connection_open(self, _unused_connection):
        LOGGER.info("Connection opened")
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        LOGGER.error("Connection open failed: %s", err)
        self._close_event.set()

    def on_connection_closed(self, _unused_connection, reason):
        if not self._closing:
            LOGGER.warning("Connection closed, reconnect necessary: %s", reason)
            self._close_event.set()

    def close(self):
        if not self._closing:
            self._closing = True
            if self._connection:
                if self._connection.is_closing or self._connection.is_closed:
                    LOGGER.info("Connection is closing or already closed")
                else:
                    LOGGER.info("Closing connection")
                    self._connection.close()
            self._close_event.set()

    def open_channel(self):
        LOGGER.info("Creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        LOGGER.info("Channel opened")
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_exchange()

    def add_on_channel_close_callback(self):
        LOGGER.info("Adding channel close callback")
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        LOGGER.info("Channel %i was closed: %s", channel, reason)
        self.close()

    def setup_exchange(self):
        LOGGER.info("Declaring exchange: %s", self.EXCHANGE)
        self._channel.exchange_declare(
            exchange=self.EXCHANGE,
            exchange_type="topic",
            durable=True,
            callback=self.on_exchange_declareok,
        )

    def on_exchange_declareok(self, _unused_frame):
        LOGGER.info("Exchange declared: %s", self.EXCHANGE)
        self.setup_queues()

    def setup_queues(self):
        for queue_route in self.queue_routes:
            LOGGER.info("Declaring queue %s", queue_route["name"])
            cb = functools.partial(
                self.on_queue_declareok,
                userdata=(queue_route["name"], "RW.%s.*" % queue_route["topic"]),
            )
            self._channel.queue_declare(
                queue=queue_route["name"], durable=True, callback=cb
            )

        self.set_qos()

    def on_queue_declareok(self, _unused_frame, userdata):
        queue_name, routing_key = userdata

        LOGGER.info("Binding %s to %s with %s", self.EXCHANGE, queue_name, routing_key)
        self._channel.queue_bind(
            queue_name,
            self.EXCHANGE,
            routing_key=routing_key,
        )

    def set_qos(self):
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok
        )

    def on_basic_qos_ok(self, _unused_frame):
        LOGGER.info("QOS set to: %d", self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        LOGGER.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()

        for queue_route in self.queue_routes:
            self._channel.basic_consume(queue_route["name"], self.on_message)

        self.was_consuming = True

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        LOGGER.info(
            "Acknowledging message %s %s",
            basic_deliver.delivery_tag,
            basic_deliver.routing_key,
        )

        # TODO do this AFTER processing the message
        self._channel.basic_ack(basic_deliver.delivery_tag)

        try:
            # 1. find route by name >> basic_deliver.routing_key
            rpc = next(
                (
                    r
                    for name, r in Router.RPCs.items()
                    if name == basic_deliver.routing_key
                ),
                None,
            )
            if not rpc:
                raise RWNotFoundException

            req = json.loads(body.decode()) if body else {}

            ""----
            (
                _,
                controller_name,
                action_name,
            ) = basic_deliver.routing_key.rsplit(".")

            route = next(
                (
                    r
                    for r in Routes
                    if r["controller_name"] == controller_name
                    and r["action_name"] == action_name
                ),
                None,
            )
            if not route:
                raise RWNotFoundException(basic_deliver.routing_key)
            ""------------

            options = req.get("options", {}) or {}
            if not "internal" in options:
                options["internal"] = True

            rpc_info = {
                "route": route,
                "params": req.get("params", {}) or {},
                "query": req.get("query", {}) or {},
                "data": req.get("data", {}) or {},
                "identity": req.get("identity", {}) or {},
                "options": options,
            }

            results = self._rpc_manager.execution_callback(rpc_info)

        except Exception as err:
            results = self._rpc_manager.error_callback(err)

        self._channel.basic_publish(
            "",  # no exchange, the queue we are sending to is exclusive
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(results, cls=CustomJsonEncoder),
        )
        LOGGER.info(
            "Received message # %s from %s, reply to %s",
            basic_deliver.delivery_tag,
            properties.app_id,
            properties.reply_to,
        )
        LOGGER.debug(
            "Body of message # %s %s",
            basic_deliver.delivery_tag,
            body,
        )

    def add_on_cancel_callback(self):
        LOGGER.info("Adding consumer cancellation callback")
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        LOGGER.info("Consumer was cancelled remotely, shutting down: %r", method_frame)
        if self._channel:
            self._channel.close()


class AmqpEngine(_RWEngine):
    def __init__(self):
        self._reconnect_delay = 0
        self._ac = _AmqpAsyncConsumer()

    def prepare_routes(self):
        for zone_controller in Router.zone_controllers:
            queue_route = {
                "name": "%s_%s_%s"
                % (
                    Config["RW_APP_NAME"],
                    Config["RW_MODULE_NAME"],
                    zone_controller,
                ),
                "topic": zone_controller,
            }
            self._ac.queue_routes.append(queue_route)

    def _check_reconnect_delay(self):
        if self._ac.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1

        if self._reconnect_delay > 30:
            self._reconnect_delay = 30

    async def run(self):
        while not self._shutdown_event.is_set():
            await self._ac.run()

            if not self._shutdown_event.is_set():
                self._check_reconnect_delay()
                LOGGER.info("Reconnecting after %d seconds", self._reconnect_delay)
                await asyncio.sleep(self._reconnect_delay)
                self._ac = _AmqpAsyncConsumer()

    def stop(self):
        self._shutdown_event.set()
        self._ac.close()

"""
