package com.example.p4ds;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;
import java.util.StringJoiner;
import java.nio.charset.StandardCharsets;

import static android.provider.ContactsContract.CommonDataKinds.Website.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    @RequiresApi(api = Build.VERSION_CODES.N)
    public void iniciarSesion(View view) throws IOException {
        EditText email;
        EditText password;

        email = findViewById(R.id.email);
        password = findViewById(R.id.password);

        /* Petición HTTP */
        // Preparamos la petición HTTP
        URL url = new URL("http://localhost:5000/login");
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");

        // Parámetros
        Map<String, String> parametros = new HashMap<>();
        String emailString = email.getText().toString();
        String passwordString = password.getText().toString();
        parametros.put("email", emailString);
        parametros.put("password", passwordString);

        con.setDoOutput(true);
        DataOutputStream out = new DataOutputStream(con.getOutputStream());
        out.writeBytes(ParameterStringBuilder.getParamsString(parametros));
        out.flush();
        out.close();

        // Cabeceras
        con.setRequestProperty("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");

        // Timeout
        con.setConnectTimeout(5000);

        /* Respuesta HTTP */
        int status = con.getResponseCode();

        if(status == 200) {
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
            String inputLine;
            StringBuffer content = new StringBuffer();
            while((inputLine = in.readLine()) != null) {
                content.append(inputLine);
            }
            in.close();
            con.disconnect();
        }

        else {
            con.disconnect();
        }
    }
}
