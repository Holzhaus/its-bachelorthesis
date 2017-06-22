using System;
using System.IO;
using System.Xml;
using Newtonsoft.Json;

public class HelloWorld
{
    static public string get_input()
    {
        string input = "";
        string s;
        while ((s = Console.ReadLine()) != null)
        {
            input += s;
        }
        return input;
    }
    static public void Main(string[] args)
    {
        string input = get_input();
        string output;
        XmlDocument doc;
        if (Array.IndexOf(args, "-d") > -1 || Array.IndexOf(args, "--decode") > -1)
        {

            doc = JsonConvert.DeserializeXmlNode(input);
            using (StringWriter sw = new StringWriter())
            using (XmlWriter tw = XmlWriter.Create(sw))
            {
                doc.WriteTo(tw);
                tw.Flush();
                output = sw.GetStringBuilder().ToString();
            }
        }
        else
        {
            doc = new XmlDocument();
            doc.LoadXml(input);
            output = JsonConvert.SerializeXmlNode(doc);
        }
        Console.WriteLine(output);
    }
}
