from typing import Optional
import requests
import threading
import time
import select

class KafkaMessageConsumer:
    def __init__(self, url, params=None, headers=None, check_interval=0.5, timeout=30):
        """
        Kafka Message Consumer to handle streaming of Kafka messages.

        Parameters
        ----------
        url : str
            The URL of the Kafka stream.
        params : dict, optional
            Parameters for the Kafka stream request (default is None).
        headers : dict, optional
            Headers to include in the request (default is None).
        check_interval : float, optional
            The interval in seconds to check for new messages (default is 0.5 seconds).
        timeout : int, optional
            Timeout for the request in seconds (default is 30 seconds).
        """
        self.url = url
        self.params = params or {}
        self.headers = headers or {}
        self.messages = []
        self._stop_event = threading.Event()
        self._check_interval = check_interval
        self._timeout = timeout
        self._thread = threading.Thread(target=self._consume_messages)
        self._thread.start()

    def _consume_messages(self):
        try:
            with requests.get(self.url, params=self.params, headers=self.headers, stream=True, timeout=self._timeout) as response:
                response.raise_for_status()
                for line in self._iter_lines_with_timeout(response):
                    if self._stop_event.is_set():
                        print("Stop event set, exiting message consumption loop.")
                        break
                    if line:
                        message = line.decode('utf-8')
                        self.messages.append(message)
        except requests.exceptions.Timeout:
            print(f"Error: Request timed out after {self._timeout} seconds.")
        except requests.exceptions.RequestException as e:
            print(f"Error consuming Kafka messages: {str(e)}")

    def _iter_lines_with_timeout(self, response):
        sock = response.raw._fp.fp.raw
        while not self._stop_event.is_set():
            ready = select.select([sock], [], [], self._check_interval)[0]
            if ready:
                line = response.raw.readline()
                if not line:
                    break
                yield line
            time.sleep(self._check_interval)

    def stop(self):
        print("Stopping consumer...")
        self._stop_event.set()
        self._thread.join()
        print("Consumer stopped.")

def consume_kafka_messages(self, id: Optional[str] = None, topic: Optional[str] = None,
                           host: Optional[str] = None, port: Optional[int] = None, timeout: int = 30) -> KafkaMessageConsumer:
    """
    Create a KafkaMessageConsumer to consume messages from a Kafka topic.

    Parameters
    ----------
    id : str, optional
        The ID of the Kafka stream.
    topic : str, optional
        The Kafka topic.
    host : str, optional
        The Kafka host.
    port : int, optional
        The Kafka port.
    timeout : int, optional
        The timeout for the request in seconds (default is 30).

    Returns
    -------
    KafkaMessageConsumer
        An instance of KafkaMessageConsumer to handle the Kafka message stream.
    """
    url = f"{self.api_url}/stream"
    params = {}
    
    if id:
        params['id'] = id
    if topic:
        params['topic'] = topic
    if host:
        params['host'] = host
    if port:
        params['port'] = port
    
    headers = self._get_headers()
    
    return KafkaMessageConsumer(url, params, headers, timeout=timeout)
