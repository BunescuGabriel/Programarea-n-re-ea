using lab_1;


namespace Lab_1
{
    class Program
    {
        public static void Main()
        {
            ServerSocket server = new ServerSocket("127.0.0.1", 5050);
            server.BindAndListen(10);
            server.AcceptAndReceive();
           
        }
    }
}
