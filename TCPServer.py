#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

global msgQuanIsTrue, msgQuan, totalPrice, msgSub, msgAddrIsTrue, addr, addrStr


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("SERVER: %s:%s has connected." % client_address)
        client.send(bytes("SERVER: Welcome to chat, please type in your name and order your food!\n", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    global msgQuanIsTrue, msgQuan, totalPrice, msgSub, msgAddrIsTrue, addr, addrStr
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'SERVER: Hello %s! For menu, type {menu}. To quit, type {quit}.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "SERVER: %s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    # as long as user don't enter {quit}, keep looping
    while True:
        # menu variables
        menu = "SERVER: Here is the menu:"
        menu2 = "1. Meatball Sub = RM10.00"
        menu3 = "2. Roasted Chicken Sub = RM 12.00"
        menu4 = "3. Vegetarian Sub = RM18.00"
        menu5 = "Please type in the food number to order"
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
            # shows the menu
            msgQuanIsTrue = 0
            if msg == bytes("{menu}", "utf8"):
                time.sleep(0.001)
                client.send(bytes(menu, "utf8"))
                time.sleep(0.001)
                client.send(bytes(menu2, "utf8"))
                time.sleep(0.001)
                client.send(bytes(menu3, "utf8"))
                time.sleep(0.001)
                client.send(bytes(menu4, "utf8"))
                time.sleep(0.001)
                client.send(bytes(menu5, "utf8"))

                # quantity
                msgSub = client.recv(BUFSIZ)
                if msgSub == bytes("1", "utf8"):
                    time.sleep(0.001)
                    client.send(bytes("SERVER: You have ordered Meatball Sub! How many?", "utf8"))
                    msgQuanIsTrue = 1
                elif msgSub == bytes("2", "utf8"):
                    time.sleep(0.001)
                    msgQuanIsTrue = 1
                    client.send(bytes("SERVER: You have ordered Roasted Chicken Sub! How many?", "utf8"))
                elif msgSub == bytes("3", "utf8"):
                    time.sleep(0.001)
                    msgQuanIsTrue = 1
                    client.send(bytes("SERVER: You have ordered Vegetarian Sub! How many?", "utf8"))
                else:
                    client.send(bytes("SERVER: Invalid input! Order cancelled.", "utf8"))
            # price calculation
            msgQuan = ""
            totalPrice = 0
            msgAddrIsTrue = 0
            if msgQuanIsTrue == 1:
                msgQuan = client.recv(BUFSIZ)
                try:
                    int(msgQuan)
                    if msgSub.decode() == "1":
                        totalPrice = int(msgQuan) * 10
                    elif msgSub.decode() == "2":
                        totalPrice = int(msgQuan) * 12
                    elif msgSub.decode() == "3":
                        totalPrice = int(msgQuan) * 18
                    time.sleep(0.001)
                    client.send(bytes("SERVER: Total price is: RM" + str(totalPrice), "utf8"))
                    msgAddrIsTrue = 1
                except:
                    client.send(bytes("SERVER: Only numbers are allowed! Order cancelled.", "utf8"))

            addrStr = ""
            # address
            if msgAddrIsTrue == 1:
                time.sleep(0.001)
                client.send(bytes("SERVER: Please key in your address ", "utf8"))
                addr = client.recv(BUFSIZ)
                addrStr = str(addr.decode())
                # display purchase info
                client.send(bytes("SERVER: Your total price: RM" + str(totalPrice), "utf8"))
                time.sleep(0.001)
                client.send(bytes("Your address: " + addrStr, "utf8"))
                time.sleep(0.001)
                client.send(bytes("A rider has been sent to your address", "utf8"))
                time.sleep(0.001)
                client.send(bytes("Thank you for ordering from Subway. To order again, type {menu}", "utf8"))

        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("SERVER: %s has left the chat." % name, "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}

HOST = ''
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
