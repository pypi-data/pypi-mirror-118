# -*- coding: utf-8 -*-
#
#      Copyright (C) 2021 Axual B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import threading
from datetime import datetime
from time import sleep
from typing import List, Tuple, Callable

import confluent_kafka.cimpl
from confluent_kafka import DeserializingConsumer as KafkaConsumer
from confluent_kafka import TopicPartition, Message
from confluent_kafka.admin import ClusterMetadata
from confluent_kafka.serialization import Deserializer

from axualclient.avro import AvroDeserializer
from axualclient.discovery import DiscoveryClient, DiscoveryClientRegistry, BOOTSTRAP_SERVERS_KEY, TIMESTAMP_KEY, \
    DISTRIBUTOR_TIMEOUT_KEY, DISTRIBUTOR_DISTANCE_KEY, SCHEMA_REGISTRY_URL_KEY, TTL_KEY
from axualclient.patterns import resolve_group, resolve_topics
from axualclient.util import first_of_string_list, filter_axual_configuration, is_documented_by

logger = logging.getLogger(__name__)

DEFAULT_POLL_SPEED = 0.2


class DeserializingConsumer(DiscoveryClient):
    """ Switching AVRO consumer.

    Implements __iter__ to be able to create a for loop on the consumer
    to iterate through messages: for msg in DeserializingConsumer.
    Set pause attribute to break from loop.
    Set poll_speed attribute to change the polling speed (default: 0.2 [secs]).
    """

    def __init__(self,
                 configuration: dict,
                 *args, **kwargs):
        """
        Instantiate an AVRO consumer for Axual. Derives from confluent_kafka
         DeserializingConsumer class.
        Note that auto-commit is set to False, so received messages must
         be committed by your script's logic.

        Parameters
        ----------
        configuration: dict
            Configuration properties including Axual Configuration. All consumer Configuration can be found at:
             https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
        *args and **kwargs :
            Other parameters that can be passed to confluent_kafka Consumer.
        """
        self.unresolved_topics = []
        self.unresolved_group_id = configuration.get('application_id')
        self.topics = []                         # have not been resolved yet
        self._consumer = None                    # no discovery result yet

        self.init_args = args
        self.init_kwargs = kwargs

        self.configuration = configuration
        # bootstrap servers & key/value serializers are not available at this point yet
        self.configuration['security.protocol'] = 'SSL'

        self.poll_speed = DEFAULT_POLL_SPEED
        self.initialized = False
        self.switch_lock = threading.Lock()
        self.init_lock = threading.Lock()

        self.discovery_result = {}
        self.discovery_fetcher = DiscoveryClientRegistry.register_client(
            self.configuration, self
        )

    def wait_for_initialization(self) -> None:
        if self.initialized:
            return
        with self.init_lock:
            self.discovery_fetcher.wait_for_discovery_result()

    def _do_with_switch_lock(self, func):
        self.wait_for_initialization()
        with self.switch_lock:
            return func()

    def _get_consumer(self):
        """ Convenience method added such that lambda expressions do not get evaluated on the old proxied object """
        return self._consumer

    def on_discovery_properties_changed(self, discovery_result: dict) -> None:
        """ A new discovery result has been received, need to switch """
        with self.switch_lock:
            self.discovery_result = discovery_result
            # plug in the new bootstrap servers
            self.configuration['bootstrap.servers'] = discovery_result[BOOTSTRAP_SERVERS_KEY]

            # plug in the resolved group.id
            self.configuration['group.id'] = resolve_group(discovery_result, self.unresolved_group_id)
            logger.debug(f'group.id: {self.configuration["group.id"]}')

            # initialize serializers against new schema registry
            sr_url = first_of_string_list(discovery_result[SCHEMA_REGISTRY_URL_KEY])

            self._reconfigure_deserializer(self.configuration['key.deserializer'], sr_url)
            self._reconfigure_deserializer(self.configuration['value.deserializer'], sr_url)

            # Switch consumer
            if self.initialized:
                assignment = self._consumer.assignment()
                self._consumer.close()

                # Calculate switch time-out
                if len(assignment) > 0:
                    switch_timeout = self._calculate_switch_timeout(discovery_result)
                    sleep(switch_timeout / 1000)

            kafka_properties = filter_axual_configuration(self.configuration)
            self._consumer = KafkaConsumer(kafka_properties, *self.init_args, **self.init_kwargs)

            # subscribe to previously subscribed-to topics, on new cluster
            if self.unresolved_topics:
                resolved_topics = resolve_topics(self.discovery_result, self.unresolved_topics)
                self._consumer.subscribe(resolved_topics)
            self.initialized = True

    def _calculate_switch_timeout(self, discovery_result):
        if self._is_at_least_once():
            return 0
        return max(int(discovery_result[DISTRIBUTOR_TIMEOUT_KEY]) *
                   int(discovery_result[DISTRIBUTOR_DISTANCE_KEY]) -
                   (datetime.utcnow() - discovery_result[TIMESTAMP_KEY]).total_seconds() * 1000,
                   int(discovery_result[TTL_KEY]))

    def _is_at_least_once(self) -> bool:
        return self.configuration.get('auto.offset.reset') in ['earliest', 'smallest', 'begin', 'start']

    def _reconfigure_deserializer(self, deserializer: Deserializer, schema_registry_url: str) -> None:
        """
        AvroDeserializers need to be reconfigured with the new target SchemaRegistry.
        @param deserializer: the deserializer to reconfigure
        @param schema_registry_url: the new SchemaRegistry url
        @return: None
        """
        if isinstance(deserializer, AvroDeserializer):
            deserializer.configure({
                'url': schema_registry_url,
                'ssl.ca.location': self.configuration['ssl.ca.location'],
                'ssl.key.location': self.configuration['ssl.key.location'],
                'ssl.certificate.location': self.configuration['ssl.certificate.location']
            })

    def __iter__(self):
        """Continuously loop through messages until self.pause is set to True"""
        self.pause = False
        while not self.pause:
            msg = self.poll(self.poll_speed)
            yield msg

    # Kafka Consumer interface
    @is_documented_by(confluent_kafka.cimpl.Consumer.assign)
    def assign(self, partitions: List[TopicPartition], *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().assign(partitions, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.assignment)
    def assignment(self, *args, **kwargs) -> List[TopicPartition]:
        return self._do_with_switch_lock(
            lambda: self._get_consumer().assignment(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.close)
    def close(self, *args, **kwargs) -> None:
        DiscoveryClientRegistry.deregister_client(self.unresolved_group_id, self)
        return self._do_with_switch_lock(
            lambda: self._get_consumer().close(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.commit)
    def commit(self,
               message: Message = None,
               offsets: List[TopicPartition] = None,
               asynchronous: bool = True,
               *args, **kwargs):
        if message is not None:
            kwargs['message'] = message
        if offsets is not None:
            kwargs['offsets'] = offsets
        kwargs['asynchronous'] = asynchronous
        return self._do_with_switch_lock(
            lambda: self._get_consumer().commit(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.committed)
    def committed(self,
                  partitions: List[TopicPartition],
                  timeout: float = None) -> List[TopicPartition]:
        if timeout is not None:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().committed(partitions, timeout)
            )
        else:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().committed(partitions)
            )

    @is_documented_by(confluent_kafka.cimpl.Consumer.consume)
    def consume(self,
                num_messages: int = 1,
                timeout: float = -1,
                *args, **kwargs) -> List[Message]:
        return self._do_with_switch_lock(
            lambda: self._get_consumer().consume(num_messages, timeout, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.consumer_group_metadata)
    def consumer_group_metadata(self):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().consumer_group_metadata()
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.get_watermark_offsets)
    def get_watermark_offsets(self,
                              partition: TopicPartition,
                              timeout: float = None,
                              cached: bool = False,
                              *args, **kwargs) -> Tuple[int, int]:
        if timeout is not None:
            kwargs['timeout'] = timeout
        return self._do_with_switch_lock(
            lambda: self._get_consumer().get_watermark_offsets(partition=partition, cached=cached, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.list_topics)
    def list_topics(self,
                    topic: str = None,
                    timeout: float = -1,
                    *args, **kwargs) -> ClusterMetadata:
        if topic is not None:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().list_topics(topic=topic, timeout=timeout, *args, **kwargs)
            )
        else:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().list_topics(timeout=timeout, *args, **kwargs)
            )

    @is_documented_by(confluent_kafka.cimpl.Consumer.offsets_for_times)
    def offsets_for_times(self,
                          partitions: List[TopicPartition],
                          timeout: float = None) -> List[TopicPartition]:
        if timeout is not None:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().offsets_for_times(partitions, timeout)
            )
        else:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().offsets_for_times(partitions)
            )

    @is_documented_by(confluent_kafka.cimpl.Consumer.pause)
    def pause(self, partitions: List[TopicPartition]) -> None:
        return self._do_with_switch_lock(
            lambda: self._get_consumer().pause(partitions)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.poll)
    def poll(self, timeout: float = None):
        if timeout is not None:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().poll(timeout)
            )
        else:
            return self._do_with_switch_lock(
                lambda: self._get_consumer().poll()
            )

    @is_documented_by(confluent_kafka.cimpl.Consumer.position)
    def position(self, partitions: List[TopicPartition]) -> List[TopicPartition]:
        return self._do_with_switch_lock(
            lambda: self._get_consumer().position(partitions)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.resume)
    def resume(self, partitions: List[TopicPartition]) -> None:
        return self._do_with_switch_lock(
            lambda: self._get_consumer().resume(partitions)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.seek)
    def seek(self, partition: TopicPartition):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().seek(partition)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.store_offsets)
    def store_offsets(self,
                      message: confluent_kafka.Message = None,
                      offsets: List[TopicPartition] = None,
                      *args, **kwargs) -> None:
        if message is not None:
            kwargs['message'] = message
        if offsets is not None:
            kwargs['offsets'] = offsets
        return self._do_with_switch_lock(
            lambda: self._get_consumer().store_offsets(message, *args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.subscribe)
    def subscribe(self,
                  topics: List[str],
                  on_assign: Callable = None,
                  on_revoke: Callable = None,
                  on_lost: Callable = None,
                  *args, **kwargs):
        self.unresolved_topics = list(set(self.unresolved_topics + topics))
        if on_assign is not None:
            kwargs['on_assign'] = on_assign
        if on_revoke is not None:
            kwargs['on_revoke'] = on_revoke
        if on_lost is not None:
            kwargs['on_lost'] = on_lost
        return self._do_with_switch_lock(
            lambda: self._get_consumer().subscribe(
                resolve_topics(self.discovery_result, topics), *args, **kwargs
            )
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.unassign)
    def unassign(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().unassign(*args, **kwargs)
        )

    @is_documented_by(confluent_kafka.cimpl.Consumer.unsubscribe)
    def unsubscribe(self, *args, **kwargs):
        return self._do_with_switch_lock(
            lambda: self._get_consumer().unsubscribe(*args, **kwargs)
        )

