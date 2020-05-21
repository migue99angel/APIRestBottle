package com.example.p4ds;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.sql.*;

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

        final EditText name = (EditText) findViewById(R.id.editText2);
        EditText password = (EditText) findViewById(R.id.editText3);

        final OkHttpClient client = new OkHttpClient();

        RequestBody cuerpo = new FormBody.Builder()
                .add("name", name.getText().toString())
                .add("password", password.getText().toString())
                .build();

        final Request request = new Request.Builder()
                .url(url)
                .post(cuerpo)
                .build();

        // Con .enqueue hacemos peticiones asíncronas
        // https://stackoverflow.com/questions/39440806/android-okhttpclient-requesting-error?rq=1
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(!response.isSuccessful()) {
                    throw new IOException("Unexpected code " + response);
                }

                // Si la consulta tiene éxito, cargamos el perfil del usuario
                try {
                    cargarPerfil(name.getText().toString());
                } catch (SQLException e) {
                    e.printStackTrace();
                } catch (ClassNotFoundException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private void cargarPerfil(String name) throws SQLException, ClassNotFoundException {
        // Consulta para obtener los datos del usuario para cargar el perfil
        Class.forName("com.mysql.jdbc.Driver");
        Connection conn = DriverManager.getConnection("jdbc:mysql://10.0.2.2:8080/p3ds", "usuario", "pass"); // !! CAMBIAR DATOS PARA LA CONEXIÓN !!
        Statement stmt = conn.createStatement();
        String query = "SELECT * FROM usuarios WHERE user=" + name;
        ResultSet rs = stmt.executeQuery(query);

        // Actualizamos la vista con lo obteido a través de la consulta

        // Cargamos la vista
        setContentView(R.layout.perfil);
    }
}
