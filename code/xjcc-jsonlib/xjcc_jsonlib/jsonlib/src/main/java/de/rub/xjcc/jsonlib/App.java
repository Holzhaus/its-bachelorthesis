package de.rub.xjcc.jsonlib;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import net.sf.json.JSON;
import net.sf.json.JSONSerializer;
import net.sf.json.xml.XMLSerializer;

/**
 * Hello world!
 *
 */
public class App
{
    public static boolean to_xml(String[] args) {
        List<String> l_args = Arrays.asList(args);
        return (l_args.contains("-d") || l_args.contains("--decode"));
    }

    public static String readString(InputStream is) {
        /*
         * I hate Java.
         * Seriously, how overly complicated can it be to read stdin into a
         * string?!
         */
        Scanner s = new Scanner(is).useDelimiter("\\A");
        return s.hasNext() ? s.next() : "";
    }

    public static void main( String[] args )
    {
        XMLSerializer xmlserializer = new XMLSerializer();
        xmlserializer.setTypeHintsEnabled(false);
        if (to_xml(args)) {
            JSON json = JSONSerializer.toJSON(readString(System.in));
            System.out.println(xmlserializer.write(json));
        } else {
            JSON json = xmlserializer.readFromStream(System.in);
            System.out.println(json.toString(2));
        }
    }
}
