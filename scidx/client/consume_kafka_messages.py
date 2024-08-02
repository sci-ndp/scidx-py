import requests
import threading
import time
import select

class KafkaMessageConsumer:
    def __init__(self, url, params, headers, check_interval=0.5):
        self.url = url
        self.params = params
        self.headers = headers
        self.messages = []
        self._stop_event = threading.Event()
        self._check_interval = check_interval
        self._thread = threading.Thread(target=self._consume_messages)
        self._thread.start()

    def _consume_messages(self):
        try:
            with requests.get(self.url, params=self.params, headers=self.headers, stream=True) as response:
                if response.status_code == 200:
                    for line in self._iter_lines_with_timeout(response):
                        if self._stop_event.is_set():
                            print("Stop event set, exiting message consumption loop.")
                            break
                        if line:
                            message = line.decode('utf-8')
                            print(f"Received message: {message}")
                            self.messages.append(message)
                else:
                    print(f"Error: Received unexpected status code {response.status_code}")
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

def consume_kafka_messages(self, topic: str) -> KafkaMessageConsumer:
    url = f"{self.api_url}/stream"
    params = {"topic": topic}
    headers = self._get_headers()
    return KafkaMessageConsumer(url, params, headers)
