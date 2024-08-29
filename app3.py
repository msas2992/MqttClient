import tkinter as tk
from tkinter import scrolledtext
import paho.mqtt.client as mqtt
import ssl

# Global MQTT client instance
client = None

# Default MQTT settings
# mqtt_settings = {
#     'host': "192.168.0.238",
#     'port': 8883,
#     'user': "tester",
#     'pass': "12345678",
#     'ca': 'C:/Program Files/mosquitto/certs/ca.crt',
#     'insecure': True,
# }

mqtt_settings = {
    'host': "localhost",
    'port': 8882,
    'user': "na",
    'pass': "na",
    'ca': 'na',
    'insecure': True,
}

topic = {
    'subscribe':"PNEWELSv1/DeviceToApp/status/#",
    'publish'  :"PNEWELSv1/AppToDevice/command/direct/01000001",
    'message'  :'{"muid":"01000001","mcommand":"STANDBY","scommand":"STANDBY"}'
}

# Function to create and configure the MQTT client
def create_mqtt_client():
    global client
    client = mqtt.Client()
    if mqtt_settings['user'] != "na":
        client.username_pw_set(username=mqtt_settings['user'], password=mqtt_settings['pass'])
    client.on_message = on_message

    if mqtt_settings['ca'] != "na":
        client.tls_set(
            ca_certs=mqtt_settings['ca'],
            certfile=None,
            keyfile=None,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2,
            ciphers=None
        )
        client.tls_insecure_set(mqtt_settings['insecure'])

# Callback when a message is received
def on_message(client, userdata, message):
    msg_text = f"\ntopic   : {message.topic} \nmessage : {message.payload.decode('utf-8')}"
    append_to_message_view(msg_text)

# Function to connect to the MQTT broker
def connect_to_broker():

    host = host_entry.get()
    port = int(port_entry.get())
    user = user_entry.get()
    password = pass_entry.get()
    ca = ca_entry.get()

    mqtt_settings['host'] = host
    mqtt_settings['port'] = port
    mqtt_settings['user'] = user
    mqtt_settings['pass'] = password
    mqtt_settings['ca'] = ca
    
    global client
    if client is None:
        create_mqtt_client()

    try:
        client.connect(mqtt_settings['host'], port=mqtt_settings['port'], keepalive=60)
        append_to_message_view(f"Connected to broker")
        client.loop_start()
    except Exception as e:
        append_to_message_view(f"Failed to connect with broker: {str(e)}")

# Function to stop the MQTT connection
def stop_connection():
    global client
    if client is not None:
        client.disconnect()
        append_to_message_view(f"Disconnected from broker")
        client = None

# Function to append text to the message view
def append_to_message_view(text):
    message_view.insert(tk.END, text + '\n')
    message_view.see(tk.END)  # Scroll to the end

# Subscribe button callback
def start_subscription():
    topic = subscripe_topic_entry.get()
    if client is not None:
        client.subscribe(topic)
        append_to_message_view(f"\nSubscribed to topic: {topic}")

# Unsubscribe button callback
def stop_subscription():
    topic = subscripe_topic_entry.get()
    if client is not None:
        client.unsubscribe(topic)
        append_to_message_view(f"\nUnsubscribed from topic: {topic}")

# Subscribe button callback
def publish():
    publish_topic = publish_topic_entry.get()
    publish_message = publish_message_entry.get("1.0", tk.END)  # Get the message from the Text widget
    print(publish_topic)
    print(publish_message)
    try:
        client.publish(publish_topic, publish_message, qos=1, retain=False)
        append_to_message_view(f"\nPublished message to topic: {publish_topic}")
    except Exception as e:
        append_to_message_view(f"\nFailed to publish message: {str(e)}")

# Tkinter application
app = tk.Tk()
app.title("MQTT Server")

# Create a frame for MQTT settings
settings_frame = tk.Frame(app)
settings_frame.pack(pady=10)


# Create Connect and Stop buttons
tk.Label(settings_frame, text="MQTT Communication Tester by Saiful, PNE Electric Sdn bhd").grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=4)

connect_button = tk.Button(settings_frame, width=11, text="Start", command=connect_to_broker)
connect_button.grid(row=1, column=1, padx=5, pady=5)

stop_button = tk.Button(settings_frame, width=11, text="Stop", command=stop_connection)
stop_button.grid(row=1, column=2, padx=5, pady=5)

# MQTT Settings labels and entry fields
tk.Label(settings_frame, text="Host:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
host_entry = tk.Entry(settings_frame, width=30)
host_entry.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
host_entry.insert(0, mqtt_settings['host'])

tk.Label(settings_frame, text="Port:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
port_entry = tk.Entry(settings_frame, width=30)
port_entry.grid(row=3, column=1, padx=5, pady=5, columnspan=2)
port_entry.insert(0, str(mqtt_settings['port']))

tk.Label(settings_frame, text="Username:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
user_entry = tk.Entry(settings_frame, width=30)
user_entry.grid(row=4, column=1, padx=5, pady=5, columnspan=2)
user_entry.insert(0, mqtt_settings['user'])

tk.Label(settings_frame, text="Password:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
pass_entry = tk.Entry(settings_frame, width=30, show="*")
pass_entry.grid(row=5, column=1, padx=5, pady=5, columnspan=2)
pass_entry.insert(0, mqtt_settings['pass'])

tk.Label(settings_frame, text="CA Cert Path:").grid(row=6, column=0, padx=5, pady=5, sticky='w')
ca_entry = tk.Entry(settings_frame, width=30)
ca_entry.grid(row=6, column=1, padx=5, pady=5, columnspan=2)
ca_entry.insert(0, mqtt_settings['ca'])

# Create Start and Stop buttons for subscription
start_subscription_button = tk.Button(settings_frame, width=24, text="Subscribe", command=start_subscription)
start_subscription_button.grid(row=1, column=4, padx=5, pady=5)

stop_subscription_button = tk.Button(settings_frame, width=24, text="Unsubscribe", command=stop_subscription)
stop_subscription_button.grid(row=1, column=5, padx=5, pady=5)

# subscription topic
tk.Label(settings_frame, text="Topic:").grid(row=2, column=3, padx=5, pady=5, sticky='w')
subscripe_topic_entry = tk.Entry(settings_frame, width=60)
subscripe_topic_entry.grid(row=2, column=4, padx=5, pady=5, columnspan=2)
subscripe_topic_entry.insert(0, topic['subscribe'])

# button publish
publish_button = tk.Button(settings_frame, width=51, text="Publish", command=publish)
publish_button.grid(row=3, column=4, padx=5, pady=5, columnspan=2)

# publish topic
tk.Label(settings_frame, text="Topic:").grid(row=4, column=3, padx=5, pady=5, sticky='w')
publish_topic_entry = tk.Entry(settings_frame, width=60)
publish_topic_entry.grid(row=4, column=4, padx=5, pady=5, columnspan=2)
publish_topic_entry.insert(0, topic['publish'])

# publish topic
tk.Label(settings_frame, text="Message:").grid(row=5, column=3, padx=5, pady=5, sticky='w')
publish_message_entry = tk.Text(settings_frame, width=45, height=3, wrap=tk.WORD)
publish_message_entry.grid(row=5, column=4, padx=5, pady=5, columnspan=2, rowspan=2)
publish_message_entry.insert(tk.END, topic['message'])


# Scrolled text widget for displaying messages
message_view = scrolledtext.ScrolledText(app, width=90, height=15)
message_view.pack(padx=15, pady=15)

app.mainloop()
