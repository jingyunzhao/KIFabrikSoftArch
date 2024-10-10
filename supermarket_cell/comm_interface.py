import socket
import threading
import queue

AgentSender = ["SupermarketocalAI", "Darko", "Stack_1", "Stack_2"]
AgentReceiver = ["SupermarketCellLocalAI", "Darko", "Stack_1", "Stack_2"]
Priority = [0, 1, 2, 3, 4]
CoodinateSystem = ["GlobalCoSys", "SupermarketocalAICoSys", "DarkoCoSys", "Stack_1CoSys", "Stack_2CoSys"]

# Predefined message catalog
msg_catalog = {}
msg_catalog["ProvideProduct"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "RequiredParts": ""
    }
}
msg_catalog["RequestCoordinate"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "RequestedAgent": "",
        "CoSys": "",
        "Coordinate": ""
    }
}
msg_catalog["ResponseCoordinate"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "RequestedAgent": "",
        "CoSys": "",
        "Coordinate": ""
    }
}
msg_catalog["RegisterSkill"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "SkillName": "",
        "SkillDescription": "",
        "Primitives": "",
        "SkillParameter": "",
        "SkillPrecondition": "",
        "SkillPostcondition": "",
        "Object": "",
        "Duration": "",
        "Goal": "",
        "SkillStatus": ""
    }
}

msg_catalog["ExecuteSkill"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "SkillName": "",
        "SkillDescription": "",
        "Primitives": "",
        "SkillParameter": "",
        "SkillPrecondition": "",
        "SkillPostcondition": "",
        "Object": "",
        "Duration": "",
        "Goal": "",
        "SkillStatus": ""
    }
}

msg_catalog["RequestSkill"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "SkillName": "",
        "SkillDescription": "",
        "Primitives": "",
        "SkillParameter": "",
        "SkillPrecondition": "",
        "SkillPostcondition": "",
        "Object": "",
        "Duration": "",
        "Goal": "",
        "SkillStatus": ""
    }
}

msg_catalog["ReportError"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "ErrorAgent": "",
        "ErrorType": "",
        "AffectedAgent": "",
        "TimeForRecovery": "",
        "ErrorRecovered": ""
    }
}

msg_catalog["InformError"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "ErrorAgent": "",
        "ErrorType": "",
        "AffectedAgent": "",
        "TimeForRecovery": "",
        "ErrorRecovered": ""
    }
}

msg_catalog["InformErrorRecovered"] = {
    "Header": {
        "Sender": "",
        "Receiver": "",
        "Priority": "",
        "Timestamp": "",
        "MsgType": ""
    },
    "Content": {
        "ErrorAgent": "",
        "ErrorType": "",
        "AffectedAgent": "",
        "TimeForRecovery": "",
        "ErrorRecovered": ""
    }
}






def handle_client_connection(client_socket):
    message_queue = queue.Queue()
    request = client_socket.recv(1024)
    print(f"Received {request}")
    message_queue.put(request)
    client_socket.send(b'ACK')
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 44))
    server.listen(5)
    print('Listening on port 44')
    
    while True:
        client_sock, address = server.accept()
        print(f"Accepted connection from {address}")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
        client_handler.start()


def send_message(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1'), 44)
    client.send(msg)

def receive_message():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1'), 44)

def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    while True:
        msg = input('Enter message to send: ')
        send_message(msg)

if __name__ == '__main__':
    main()
    