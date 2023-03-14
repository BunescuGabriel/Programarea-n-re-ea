using client;

Console.WriteLine("Hello, World!");

ClientSocket client = new ClientSocket();
client.Connect("127.0.0.1", 5050);
client.SendLoop();

