from google.cloud import pubsub_v1
from google.cloud import datastore
import time

project_id = 'tatvic-gcp-dev-team'
topic_name='server_side_tagging_pubsub'
store_id=[]
subscription_name='server-side-tagging-sub'
datastore_client = datastore.Client()

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(project_id,topic_name)
message_data='12121'
future = publisher.publish(topic_path, data=message_data.encode("utf-8"))
future.result()

print("Published message to Pub/Sub:", message_data)


  
# time.sleep(5)
# def receive_single_message(project_id, subscription_name):
    
# subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(project_id, subscription_name)

num_messages = 1

response = subscriber.pull(subscription=subscription_path, max_messages=num_messages)

for received_message in response.received_messages:
    try:
        print(f"Received messagee: {received_message.message.data}")
        store_id.append(received_message.message.data.decode('utf-8'))

        subscriber.acknowledge(
        subscription=subscription_path,
        ack_ids=[received_message.ack_id],
        )        
    except Exception as e:
        print(f"Error processing or acknowledging the message: {e}")


# receive_single_message(project_id,subscription_name)
print('-------',store_id)





