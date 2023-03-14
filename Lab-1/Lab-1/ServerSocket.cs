using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace lab_1
{
    class ServerSocket
    {
        private readonly Socket _serverSocket;
        private readonly IPEndPoint _serverEndPoint;
        private readonly List<Socket> _clients = new List<Socket>();
        private readonly object _clientsLock = new object();

        public ServerSocket(string ip, int port)
        {
            IPAddress ipAddress = IPAddress.Parse(ip);

            _serverSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            _serverEndPoint = new IPEndPoint(ipAddress, port);
        }
        public void BindAndListen(int queueLimit)
        {
            try
            {
                _serverSocket.Bind(_serverEndPoint);
                _serverSocket.Listen(queueLimit);
                Console.WriteLine($"Server listening on {_serverEndPoint}");
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error binding and listening:{e.Message}");
            }

        }
        public void AcceptAndReceive()
        {
            while (true)
            {
                Socket client = acceptClient();

                if (client != null)
                {
                    lock (_clientsLock)
                    {
                        _clients.Add(client);
                    }
                    Thread clientThread = new Thread(() => receiveLoop(client));
                    clientThread.Start();
                }
            }
        }
        private Socket acceptClient()
        {
            Socket client = null;
            try
            {
                client = _serverSocket.Accept();
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error accepting: {e.Message}");
            }
            return client;
        }

        private void receiveLoop(Socket client)
        {
            while (true)
            {
                try
                {
                    byte[] buffer = new byte[1024];
                    int bytesReceived = client.Receive(buffer);
                    string text = Encoding.UTF8.GetString(buffer);

                    Console.WriteLine($"From {client.RemoteEndPoint} - {text}");

                    // Trimite mesajul către toți clienții conectați, cu excepția celui care a trimis mesajul
                    Thread sendThread = new Thread(() =>
                    {
                        lock (_clientsLock)
                        {
                            foreach (Socket otherClient in _clients)
                            {
                                if (otherClient != client)
                                {
                                    otherClient.Send(buffer);
                                }
                            }
                        }
                    });
                    sendThread.Start();

                }
                catch (SocketException se)
                {
                    if (se.SocketErrorCode == SocketError.ConnectionReset)
                    {
                        Console.WriteLine($"Client {client.RemoteEndPoint} disconnected.");
                    }
                    else
                    {
                        Console.WriteLine($"Error receiving from {client.RemoteEndPoint}: {se.Message}");
                    }
                    break;
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error receiving from {client.RemoteEndPoint}: {e.Message}");
                    break;
                }
            }

            lock (_clientsLock)
            {
                _clients.Remove(client);
                client.Close();
            }
        }

    }
}
