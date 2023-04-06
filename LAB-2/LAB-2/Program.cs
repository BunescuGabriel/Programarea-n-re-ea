using LAB_2;
using System;

namespace Lab2
{
    class Program
    {
        static void Main(string[] args)
        {
            string multicastIP = "239.5.6.7";
            int port = 5002;

            Console.Write("Enter your username: ");
            string username = Console.ReadLine();

            UDPChat chat = new UDPChat(multicastIP, port);

            chat.StartReceiveLoop();

            Console.WriteLine("Input format: <IP>:<TEXT>");
            Console.WriteLine("IP=0 - MULTICAST");
            //adaugat try, catch 
            while (true)
            {
                var input = Console.ReadLine() ?? "";
                var splitted = input.Split(':');
                var toIP = splitted[0];
                var text = splitted[1];

                if (toIP != "0")
                {
                    chat.SendTo(toIP, username + ": " + text);
                }
                else
                {
                    chat.SendGeneral(username + ": " + text);
                    Console.WriteLine($"Sent to multicast group: {text}");
                }
            }
        }
    }
}