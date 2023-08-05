import asyncio
from logging import Logger
from deepmerge import always_merger
from delphai_utils.logging import default_config, logging
from abc import abstractmethod, abstractproperty
import faust
from dataclasses import dataclass, field
from typing import Dict, List, Optional, TypeVar, Type
from delphai_utils.config import get_config
from faust.types import CodecArg
from faust.types.models import ModelT
from faust.streams import Stream
from confluent_kafka.admin import AdminClient, NewTopic
from betterproto import Message
from faust.serializers import Codec
from dacite import from_dict
from delphai_utils.config import get_config
import coloredlogs


@dataclass
class Step:
  name: str
  partitions: int
  output: Optional[str]
  tables: Optional[List[str]] = field(default_factory=lambda: [])


T = TypeVar("T")


class FaustProtobufSerializer(Codec):
  def __init__(self, type_class: T, **kwargs):
    self.type_class = type_class
    super(FaustProtobufSerializer, self).__init__(type_class=type_class, **kwargs)

  def _loads(self, s: bytes) -> T:
    return self.type_class().from_json(s.decode('utf-8'))

  def _dumps(self, s: Message) -> bytes:
    return s.to_json().encode('utf-8')


class FaustAgent():
  step: str
  step_config: Step
  agent_id: str
  input_topic: faust.TopicT
  output_topic: faust.TopicT
  input_value_type: Type[ModelT]
  output_value_type: Type[ModelT]
  input_value_serializer: CodecArg
  output_value_serializer: CodecArg
  agent: faust.Agent
  logger: Logger

  @abstractproperty
  def step(self) -> str:
    pass

  @abstractproperty
  def input_value_type(self) -> Type[ModelT]:
    pass

  @abstractproperty
  def output_value_type(self) -> Type[ModelT]:
    pass

  @abstractproperty
  def input_value_serializer(self) -> CodecArg:
    pass

  @abstractproperty
  def output_value_serializer(self) -> CodecArg:
    pass

  @abstractmethod
  async def process(self, requests: Stream[Type[ModelT]]):
    pass

  async def on_start(self):
    self.logger.info(f'started agent {self.agent_id}')

  async def after_attach(self):
    pass


class FaustApp():
  app: faust.App
  worker: faust.Worker
  logging_config: Dict

  async def on_startup_finished(self):
    self.logger.info(f'started app {self.app._conf.id}')

  async def on_start(self):
    self.logger.info(f'starting app {self.app._conf.id}')

  async def on_shutdown(self):
    self.logger.info(f'shutting down {self.app._conf.id}')

  def on_setup_root_logger(self, logger: logging.Logger, level: int):
    standard_format = self.logging_config['formatters']['standard']
    effective_level = self.logger.getEffectiveLevel()
    logger.setLevel(effective_level)
    coloredlogs.install(
      level=effective_level,
      fmt=standard_format['format'],
      datefmt=standard_format['datefmt'],
      logger=logger,
    )
    self.worker._disable_spinner_if_level_below_WARN(effective_level)
    self.worker._setup_spinner_handler(logger, effective_level)

  def __init__(self, id: str, broker: str) -> None:
    self.app = faust.App(id=id, broker=broker, web_enabled=False)
    loop = asyncio.get_event_loop()
    provided_config = {}
    try:
      provided_config = get_config('logging')
    except Exception:
      pass
    default_config['disable_existing_loggers'] = False
    default_config['formatters']['standard']['format'] = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
    default_config['loggers']['faust'] = {'level': logging.ERROR}
    default_config['loggers']['aiokafka'] = {'level': logging.ERROR}
    default_config['loggers']['mode'] = {'level': logging.ERROR}
    self.logging_config = always_merger.merge(default_config, provided_config)
    self.worker = faust.Worker(self.app, loop=loop, loglevel=logging.INFO, logging_config=self.logging_config)
    self.worker.on_startup_finished = self.on_startup_finished
    self.worker.on_start = self.on_start
    self.worker.on_shutdown = self.on_shutdown
    self.worker.on_setup_root_logger = self.on_setup_root_logger
    self.logger = logging.getLogger(self.app._conf.id)

  def start(self, agents: List[FaustAgent]):
    try:
      broker = str(self.app._conf.broker[0])
      steps = list(map(lambda s: s['name'], get_config('steps')))
      for step in steps:
        self.create_topic(broker, step)
      tasks = []
      for agent in agents:
        tasks.append(self.attach(agent))
      self.worker.loop.run_until_complete(asyncio.gather(*tasks))
      self.worker.execute_from_commandline()
    except KeyboardInterrupt:
      self.logger.info('keyboard interrupt received')

  def get_step_config(self, step: str) -> Step:
    step_config = next((s for s in get_config('steps') if s['name'] == step), None)
    return from_dict(data_class=Step, data=step_config)

  def create_topic(self, broker: str, step: str):
    step_config = self.get_step_config(step)
    client = AdminClient({'bootstrap.servers': broker.replace('kafka://', '')})
    topics = list(client.list_topics().topics.keys())
    topic_names = [f'{self.app._conf.id}.{step_config.name}']
    for table in step_config.tables:
      table_topic_name = f'{self.app._conf.id}-{table}-changelog'
      topic_names.append(table_topic_name)
    for topic_name in topic_names:
      if topic_name not in topics:
        self.logger.info(f'creating topic {topic_name} with {step_config.partitions} partitions')
        resp = client.create_topics([NewTopic(topic_name, step_config.partitions, 1)])
        resp[topic_name].result()
      else:
        self.logger.info(f'topic {topic_name} already exists')

  async def attach(self, agent: FaustAgent):
    agent.step_config = self.get_step_config(agent.step)
    agent.agent_id = f'{self.app._conf.id}.{agent.step}'
    agent.logger = logging.getLogger(f'{self.app._conf.id}] [{agent.step}')
    agent.input_topic = self.app.topic(
      agent.agent_id,
      value_type=agent.input_value_type,
      value_serializer=agent.input_value_serializer,
    )
    output_topic_name = f'{self.app._conf.id}.{agent.step_config.output}'
    agent.output_topic = self.app.topic(
      output_topic_name,
      value_serializer=agent.output_value_serializer,
    )
    new_agent = self.app.agent(agent.input_topic)(agent.process)
    agent.agent = new_agent
    await agent.after_attach()
    await new_agent.start()
