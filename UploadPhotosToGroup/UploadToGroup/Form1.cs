using System;
using System.IO;
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
            var vk = new VK_API();
            var files = Directory.GetFiles(folderBrowserDialog1.SelectedPath);
            for (int i=0; i < files.Length; i++)
            {
                for (int j = 0; j <= 100; j++)
                {
                    try
                    {
                        var response = vk.Upload(textBox2.Text, textBox3.Text, textBox1.Text, files[i]);
                        if (response["response"].ToString() != null)
                        {
                            break;
                        }
                        else if (response["error"].ToString() != null)
                        {
                            label5.Text = response["error"]["error_msg"].ToString();
                            label5.Refresh();
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
    }

    class VK_API
    {
        string v = "5.92";

        //осуществляет вызов метода vk api
        public JObject Upload(string groupid, string albumid, string token, string imagePath)
        {
            var c = new WebClient();
            //
            var u = "https://api.vk.com/method/photos.getUploadServer?group_id=" + groupid
                    + "&album_id=" + albumid
                    + "&access_token=" + token
                    + "&v=" + v;
            var r = c.DownloadString(u);
            var j = JsonConvert.DeserializeObject(r) as JObject;
            //
            var u2 = j["response"]["upload_url"].ToString();
            var r2 = Encoding.UTF8.GetString(c.UploadFile(u2, "POST", imagePath));
            var j2 = JsonConvert.DeserializeObject(r2) as JObject;
            //
            var u3 = "https://api.vk.com/method/photos.save?access_token=" + token
                     + "&group_id=" + groupid
                     + "&album_id=" + albumid
                     + "&server=" + j2["server"]
                     + "&photos_list=" + j2["photos_list"]
                     + "&aid=" + j2["aid"]
                     + "&hash=" + j2["hash"];
            var res = c.DownloadString(u3);
            return JsonConvert.DeserializeObject(res) as JObject;
        }
    }
}
