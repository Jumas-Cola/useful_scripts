using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Text;
using System.Windows.Forms;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace UploadToGroup
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            var vk = new VK_API(textBox1.Text);
            var files = Directory.GetFiles(folderBrowserDialog1.SelectedPath);
            var date = DateTimeOffset.UtcNow.ToUnixTimeSeconds();
            JObject response;
            string photo_obj;
            string owner_id = "";

            for (int i=0; i < files.Length; i++)
            {
                for (int j = 0; j <= 100; j++)
                {
                    try
                    {
                        response = vk.Upload(textBox2.Text, files[i]);
                        if (response["response"].ToString() != null)
                        {
                            photo_obj = String.Format("photo{0}_{1}",
                                response["response"][0]["owner_id"].ToString(),
                                response["response"][0]["id"].ToString());
                            if (textBox2.Text != "")
                            {
                                owner_id = "-" + textBox2.Text;
                            }
                            else
                            {
                                owner_id = response["response"][0]["owner_id"].ToString();
                            }
                            Dictionary<string, string> parameters = new Dictionary<string, string>
                            {
                                {"owner_id" , owner_id},
                                {"message" , textBox3.Text},
                                {"attachments" , photo_obj},
                                {"from_group" , "1"},
                                {"signed" , "0"},
                                {"publish_date" , date.ToString()}
                            };
                            vk.Method("wall.post", parameters);
                            date += 60 * Convert.ToInt32(comboBox1.Text);
                            break;
                        }
                        if (j == 100)
                        {
                            Application.Exit();
                        }
                        System.Threading.Thread.Sleep(j * 50);
                    }
                    catch (Exception ex)
                    {
                        label5.Text = ex.ToString();
                        label5.Refresh();
                    }
                }
                if (checkBox1.Checked)
                {
                    File.Delete(files[i]);
                }
                label5.Text = "Загружено: "+ i.ToString()+" / "+ files.Length.ToString();
                label5.Refresh();
            }
            label5.Text = "Готово!";
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (folderBrowserDialog1.ShowDialog() == DialogResult.OK)
            {
                label4.Text = folderBrowserDialog1.SelectedPath;
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }

    class VK_API
    {
        private string v = "5.92";
        private string token;

        public VK_API(string token) {
            this.token = token;
        }

        // загрузка фото на стену
        public JObject Upload(string group_id, string imagePath)
        {
            var c = new WebClient();
            var u = "https://api.vk.com/method/photos.getWallUploadServer?"
                    + "group_id=" + group_id
                    + "&access_token=" + token
                    + "&v=" + v;
            var r = c.DownloadString(u);
            var j = JsonConvert.DeserializeObject(r) as JObject;
            var u2 = j["response"]["upload_url"].ToString();
            var r2 = Encoding.UTF8.GetString(c.UploadFile(u2, "POST", imagePath));
            var j2 = JsonConvert.DeserializeObject(r2) as JObject;
            var u3 = "https://api.vk.com/method/photos.saveWallPhoto?"
                     + "group_id=" + group_id
                     + "&server=" + j2["server"]
                     + "&photo=" + j2["photo"]
                     + "&hash=" + j2["hash"]
                     + "&access_token=" + token
                     + "&v=" + v;
            var res = c.DownloadString(u3);
            return JsonConvert.DeserializeObject(res) as JObject;
        }

        // метод vk api
        public JObject Method(string method, Dictionary<string, string> parameters) {
            var c = new WebClient();
            parameters.Add("access_token", token);
            parameters.Add("v", v);
            var url = "https://api.vk.com/method/" + method;
            url = string.Format(url + "?{0}", 
                string.Join("&", 
                    parameters.Select(kvp => 
                        string.Format("{0}={1}", kvp.Key, kvp.Value))));
            var res = c.DownloadString(url);
            return JsonConvert.DeserializeObject(res) as JObject;
        }
    }
}
