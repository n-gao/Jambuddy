import websockets as ws
import asyncio
import json
from methods import methods

"""List containing all active connections
"""
connections = []

""" Represents a Websocket connection; 
    has a queue of messages which will be sent
"""
class WebsocketConnection:
    def __init__(self, websocket, path):
        self.socket = websocket
        self.path = path
        self.queue = asyncio.Queue()


    """ forwards incoming messages to 'consume'
    """
    async def consume_handler(self):
        try:
            while True:
                msg = await self.socket.recv()
                await self.consume(msg)
        except:
            pass


    """Queries 'produce' to get the next message and sents it.
    """
    async def produce_handler(self):
        try:
            while True:
                msg_obj = await self.produce()
                print(msg_obj)
                msg = json.dumps(msg_obj)
                await self.socket.send(msg)
        except:
            pass


    """ Handles incoming messages.
        Any incoming message must be a JSON object with an attribute called 'method'.
        The method attribute is used to determine the called method from 'methods.py'.
    """
    async def consume(self, msg):
        msg_obj = None
        # Parse JSON Object
        try:
            msg_obj = json.loads(msg)
        except:
            await self.throw_error('%s\n is no JSON object!' % msg)
            return
        # Check if the 'method' entry exists
        if 'method' not in msg_obj:
            await self.throw_error('%s has no attribute \'method\'' % msg_obj)
            return
        # Try calling the specified method
        try:
            result = await methods[msg_obj['method']](msg_obj)
            if result is not None:
                await self.queue.put(result)
        except:
            await self.throw_error('Method %s does not exists' % msg_obj['method'])
        print('Handled request:\n %s' % msg_obj)


    """Gets the next message from the queue and returns it.

    Returns:
        Object -- Next message to send
    """
    async def produce(self):
        msg = await self.queue.get()
        return msg


    """Help method to print an error to both sides of the connection. 
    """
    async def throw_error(self, error):
        print(error)
        await self.queue.put(error)


""" Handler for incoming connections.
    Creates a WebsocketConnection and start the consume and produce handler.
    If this methods exists the connection will be closed.
"""
async def handler(websocket, path):
    #Create new WebsocketConnection
    connection = WebsocketConnection(websocket, path)
    connections.append(connection)
    address = websocket.remote_address[0]
    print('Established a connection to %s' % address)
    #Start conume and produce procedures
    consumer_task = asyncio.ensure_future(connection.consume_handler())
    producer_task = asyncio.ensure_future(connection.produce_handler())
    _, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when = asyncio.FIRST_COMPLETED
    )
    #If one failes kill the remaining ones
    for task in pending:
        task.cancel()
    connections.remove(connection)
    print('Closed connection to %s' % address)


"""Creates a websocket server with the given handler on the given port.
"""
def start_server(handler, port):
    asyncio.get_event_loop().run_until_complete(
        ws.serve(handler, 'localhost', port)
    )
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    start_server(handler, 8888)
