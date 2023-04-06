using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace client
{
    public class ClientSocket
    {
        private readonly Socket _clientSocket;
        private bool _running = true;
        public ClientSocket()
        {
            _clientSocket = new Socket(AddressFamily.InterNetwork,
                SocketType.Stream, ProtocolType.Tcp);
        }

        public void Connect(string remoteIp, int remotePort)
        {
            var ipAddress = IPAddress.Parse(remoteIp);
            var endPoint = new IPEndPoint(ipAddress, remotePort);

            try
            {
                _clientSocket.Connect(endPoint);

                // Începeți un fir nou pentru a primi mesaje de la server
                Task.Run(() => ReceiveMessages());
            }
            catch (Exception e)
            {
                Console.WriteLine($"Error connecting: {e.Message}");
            }
        }

        public void SendLoop()
        {
            Console.Write("Enter your username: ");
            string username = Console.ReadLine() ?? "";

            while (_running)
            {
                try
                {
                    Console.Write("Enter message: ");
                    string text = Console.ReadLine() ?? "";

                    // Construiți mesajul de trimis către server
                    string message = $"{username}: {text}";

                    byte[] buffer = Encoding.UTF8.GetBytes(message);
                    _clientSocket.Send(buffer);
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error sending: {e.Message}");
                }
            }
        }

        private void ReceiveMessages()
        {
            while (_running)
            {
                try
                {
                    byte[] buffer = new byte[1024];
                    int receivedBytes = _clientSocket.Receive(buffer);

                    // Imprimă o linie goală înainte de mesajul primit
                    Console.WriteLine();

                    string response = Encoding.UTF8.GetString(buffer, 0, receivedBytes);
                    Console.WriteLine(response);

                    Console.Write("Enter message: ");
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error receiving: {e.Message}");
                }
            }
        }

        public void Stop()
        {
            _running = false;
            _clientSocket.Close();
        }
    }
}