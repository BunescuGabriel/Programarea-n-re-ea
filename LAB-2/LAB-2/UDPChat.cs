using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace LAB_2
{
    public class UDPChat
    {
        private int _port;
        private string _multicastIP;
        private Socket _multicastSocket;
        private Socket _senderSocket;

        public UDPChat(string multicastIP, int port)
        {
            _port = port;
            _multicastIP = multicastIP;

            var hostIP = new IPEndPoint(IPAddress.Any, port);
            _multicastSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

            _multicastSocket.Bind(hostIP);
            _multicastSocket.SetSocketOption(SocketOptionLevel.IP, SocketOptionName.AddMembership,
                 new MulticastOption(IPAddress.Parse(multicastIP), IPAddress.Any));

            _senderSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

            _senderSocket.SetSocketOption(SocketOptionLevel.IP, SocketOptionName.AddMembership,
                 new MulticastOption(IPAddress.Parse(multicastIP), IPAddress.Any));

            _senderSocket.SetSocketOption(SocketOptionLevel.IP, SocketOptionName.MulticastTimeToLive, 50);
        }

        public void StartReceiveLoop()
        {
            Thread thread = new Thread(new ThreadStart(receive));

            thread.Start();
        }

        public void SendTo(string ip, string text)
        {
            IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Parse(ip), _port);

            byte[] bytes = Encoding.UTF8.GetBytes(text);
            _senderSocket.SendTo(bytes, remoteEndPoint);
        }

        public void SendGeneral(string text)
        {
            IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Parse(_multicastIP), _port);

            string message = $"{text}\n"; // add newline character to the end of the message
            byte[] bytes = Encoding.UTF8.GetBytes(text);
            _senderSocket.SendTo(bytes, remoteEndPoint);
        }

        private void receive()
        {
            while (true)
            {
                byte[] buffer = new byte[1024];
                EndPoint remoteClient = new IPEndPoint(0, 0);

                _multicastSocket.ReceiveFrom(buffer, ref remoteClient);
                string text = Encoding.UTF8.GetString(buffer);
                Console.WriteLine($"Received from: {remoteClient} : {text}");
            }
        }

    }
}


