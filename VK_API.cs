using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Threading.Tasks;
using System.IO;
// Далее ваши библиотеки
using Newtonsoft.Json;

namespace Vk
{
    class Program
    {
        static void Main(string[] args)
        {
            var vk = new VK_API();
            string path = @"token.txt";
            string token;
            // получаем токен
            if (!File.Exists(path))
            {
                token = vk.getToken("kbbyfl8@yandex.ru", "U*s1j4Ves2k@", "3140623", "VeWdmVclDCtn6ihuP1nt");
                File.WriteAllText(path, token, Encoding.Default);
            }
            else
            {
                StreamReader tr = new StreamReader(path);
                token = tr.ReadLine();
                tr.Close();
            }
            Console.WriteLine(token);
            //выполняем вызов метода vk api
            var res = vk.vkMethod("wall.get", new Dictionary<string, string>
            {
                {"owner_id", "1"},
                {"count", "1"},
                {"filter", "owner"},
                { "v", "5.80" },
                { "access_token", token }
            });
            Console.WriteLine(res["response"]);
        }
    }

    class VK_API
    {
        //возвращает токен прямой авторизации пользователя
        public string getToken(string login, string pass, string clientID, string clientSecret)
        {
            string url = "https://oauth.vk.com/token?";
            List<string> get_params = new List<string>();
            get_params.Add(String.Concat("grant_type=","password"));
            get_params.Add(String.Concat("client_id=", clientID));
            get_params.Add(String.Concat("client_secret=", clientSecret));
            get_params.Add(String.Concat("username=", login));
            get_params.Add(String.Concat("password=", pass));
            get_params.Add(String.Concat("v=", "5.37"));
            get_params.Add(String.Concat("2fa_supported=", "1"));
            string request = String.Concat(url,String.Join("&", get_params));
            WebClient client = new WebClient();
            client.Encoding = Encoding.UTF8;
            var json = client.DownloadString(request);
            var values = JsonConvert.DeserializeObject<Dictionary<string, string>>(json);
            return values["access_token"];
        }

        //осуществляет вызов метода vk api
        public Dictionary<string, object> vkMethod(string method, Dictionary<string, string> dict)
        {
            string request = "https://api.vk.com/method/";
            request = String.Concat(request, method,"?");
            foreach (KeyValuePair<string, string> entry in dict)
            {
                request = String.Concat(request, entry.Key, "=", entry.Value, "&");
            }
            request = request.TrimEnd(new Char[] {'&'});
            WebClient client = new WebClient();
            client.Encoding = Encoding.UTF8;
            var json = client.DownloadString(request);
            var values = JsonConvert.DeserializeObject<Dictionary<string, object>>(json);
            return values;
        }
    }
}
