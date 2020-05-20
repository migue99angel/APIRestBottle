package com.example.p4ds;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import static android.provider.ContactsContract.CommonDataKinds.Website.URL;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void iniciarSesion(View view) {
        String url = "http://10.0.2.2:5000/login"; // Hay que usar esta IP para referirnos a nuestra propia máquina y no al propio emulador

        TextView name = (TextView) findViewById(R.id.textView2);
        TextView password = (TextView) findViewById(R.id.textView3);

        OkHttpClient client = new OkHttpClient();

        RequestBody cuerpo = new FormBody.Builder()
                .add("name", name.getText().toString())
                .add("password", password.getText().toString())
                .build();

        Request request = new Request.Builder()
                .url(url)
                .post(cuerpo)
                .build();

        try(Response response = client.newCall(request).execute()) {
            if(!response.isSuccessful()) throw new IOException("Unexpected code " + response);

            // Si la consulta tiene éxito, cargamos el perfil del usuario
            this.cargarPerfil(name.getText().toString());
        } catch (ClassNotFoundException | SQLException | IOException e) {
            e.printStackTrace();
        }
    }

    private void cargarPerfil(String name) throws SQLException, ClassNotFoundException {
        // Consulta para obtener los datos del usuario para cargar el perfil
        Class.forName("com.mysql.jdbc.Driver");
        Connection conn = DriverManager.getConnection("jdbc:mysql://10.0.2.2:8080/P3DS", "usuario", "pass"); // !! CAMBIAR DATOS PARA LA CONEXIÓN !!
        Statement stmt = conn.createStatement();
        String query = "SELECT * FROM usuarios WHERE user=" + name;
        ResultSet rs = stmt.executeQuery(query);

        // Actualizamos la vista con lo obteido a través de la consulta

        // Cargamos la vista
        setContentView(R.layout.perfil);
    }
}
