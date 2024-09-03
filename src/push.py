from firebase_admin import messaging


def send_to_fcm(token: str, title: str, description: str):
    # This registration token comes from the client FCM SDKs.
    registration_token = token

    # See documentation on defining a message payload.
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=description,
        ),
        token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print("Successfully sent message:", response)
