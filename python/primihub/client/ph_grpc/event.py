"""
 Copyright 2022 Primihub

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 """

from primihub.client.tiny_listener import Listener
from primihub.client.ph_grpc.task import Task
from primihub.client.tiny_listener import Event
from primihub.utils.logger_util import logger

listener = Listener()
listener.run()


@listener.on_event("/0/")
def node_event_handler(event: Event):
    from primihub.client import primihub_cli as cli
    cli.notify_channel_connected = True
    # self.notify_channel_connected = True
    logger.debug("node_event_handler: %s" % event)


@listener.on_event("/1/{task_id}")
async def handler_task_status(event: Event):
    task_id = event.params["task_id"]
    logger.debug("handler_task_status params: {}, data: {}".format(event.params, event.data))
    # TODO
    # event data
    # {'event_type': 1,
    #      'task_status': {'task_context': {'task_id': '1',
    #                                       'job_id': 'task test status'
    #                                       }
    #                   'status': '' // ? TODO
    #                      }
    #      }
    # node = ""  # TODO
    # cert = ""  # TODO
    nodes = [
        {
            "client_id": "192.168.99.23",
            "client_ip": 6667,
            "client_port": 10051
        },
        {
            "client_id": "192.168.99.23",
            "client_ip": 6668,
            "client_port": 10052

        }
    ]
    from primihub.client import primihub_cli as cli
    for node in nodes:
        connect_str = node['client_id'] + ":" + str(node["client_ip"])
        cert = ""  # TODO

        logger.debug("node connect str: {}".format(connect_str))
        task = Task(task_id=task_id, primihub_client=cli)
        logger.debug("task id: {}".format(task_id))
        task.get_node_event(node=connect_str, cert=cert)
    
    task_status = event.data.task_status.status
    task.set_task_status(task_status)



@listener.on_event("/2/{task_id}")
async def handler_task_result(event: Event):
    logger.debug("handler_task_result", event.params, event.data)

    ...
    # event data
    # {'event_type': 2,
    #  'task_result': {'task_context': {'task_id': '1',
    #                                   'job_id': 'task test result'},
    #                   'result_dataset_url': '' // ? TODO
    #                  }
    #  }
