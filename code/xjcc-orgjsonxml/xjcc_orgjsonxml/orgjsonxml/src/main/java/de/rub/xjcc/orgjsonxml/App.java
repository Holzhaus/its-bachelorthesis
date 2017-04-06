package de.rub.xjcc.orgjsonxml;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import org.json.JSONObject;
import org.json.XML;

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
        String data = readString(System.in);
        if (to_xml(args)) {
            JSONObject json = new JSONObject(data);
            System.out.print(XML.toString(json));
        } else {
            JSONObject json = XML.toJSONObject(data);
            System.out.print(json.toString());
        }
    }
}
