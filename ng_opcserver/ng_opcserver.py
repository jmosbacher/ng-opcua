# -*- coding: utf-8 -*-
from asyncua import ua, Server
from asyncua.common import node
from asyncua.common.methods import uamethod
from enum import IntEnum
import asyncio
import random
import logging
import time

# Not required just for convenience
# Because this example is based on EnumStrings, the values should start at 0 and no gaps are allowed.
class GeneratorState(IntEnum):
    off = 0     # No communication
    idle = 1    # Communication established, run settings not set
    ready = 2   #run settings set, ready to start running
    running = 3 # producing neutrons

# helper method to automatically create string list
def enum_to_stringlist(a_enum):
    items = []
    for value in a_enum:
        items.append(ua.LocalizedText(value.name))
    return items

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


@uamethod
def func(parent, value):
    return value * 2

async def serve_state(duration=None, frequency=1, debug=False):
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/pulsedng/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://pulsedng.xenon-sc.lngs.infn.it"
    nsidx = await server.register_namespace(uri)

    # --------------------------------------------------------
    # create custom enum data type
    # --------------------------------------------------------
    enums = await server.get_root_node().get_child(["0:Types", "0:DataTypes", "0:BaseDataType", "0:Enumeration"])

    # 1.
    # Create Enum Type
    GeneratorState_type = await enums.add_data_type(nsidx, 'GeneratorState')

    # Or convert the existing IntEnum GeneratorState
    es = await GeneratorState_type.add_property(0, "EnumStrings" , enum_to_stringlist(GeneratorState))

    await es.set_value_rank(1)
    await es.set_array_dimensions([0])

    # --------------------------------------------------------
    # create object with enum variable
    # --------------------------------------------------------
    # get Objects node, this is where we should put our custom stuff
    objects = server.get_objects_node()

    # create object
    myobj = await objects.add_object(nsidx, 'GeneratorObject')

    # add var with as type the custom enumeration
    GeneratorState_var = await myobj.add_variable(nsidx, 'GeneratorState2Var', GeneratorState.off, datatype = GeneratorState_type.nodeid)
    await GeneratorState_var.set_writable()
    await GeneratorState_var.set_value(GeneratorState.idle)  # change value of enumeration

    _logger.info('Starting server!')
    async with server:
        while True:
            for state in GeneratorState:
                await asyncio.sleep(2)
                _logger.info('Set value of %s to %d', GeneratorState_var, state)
                await GeneratorState_var.set_value(state)

def run_server(duration, frequency, debug):
    loop = asyncio.get_event_loop()
    loop.set_debug(debug)
    loop.run_until_complete(serve_state(duration, frequency, debug))
    loop.close()

if __name__ == "__main__":
    run_server(100, 1, True)
