import asyncio
import sys
sys.path.insert(0, "..")
import logging
from asyncua import Client, Node, ua

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger('asyncua')


async def poll_status(duration=10, frequency=1):
    url = 'opc.tcp://0.0.0.0:4840/pulsedng/'
    # url = 'opc.tcp://commsvr.com:51234/UA/CAS_UA_Server'
    async with Client(url=url) as client:
        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        _logger.info('Objects node is: %r', root)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        _logger.info('Children of root are: %r', await root.get_children())

        uri = 'http://pulsedng.xenon-sc.lngs.infn.it'
        idx = await client.get_namespace_index(uri)

        for _ in range(int(duration/frequency)):
            var = await root.get_child(["0:Objects", f"{idx}:GeneratorObject", f"{idx}:GeneratorState2Var"])
            val = await var.get_value()
            print("GeneratorState2Var", var, val)
            await asyncio.sleep(1/frequency)

def run_poll_status(duration, frequency, debug):
    loop = asyncio.get_event_loop()
    loop.set_debug(debug)
    loop.run_until_complete(poll_status(duration, frequency))
    loop.close()

if __name__ == '__main__':
    run_poll_status(10,1,True)