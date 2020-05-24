package com.example.p4ds;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

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

    private boolean identificado = false;
    private String email = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void iniciarSesion(View v) {
        String url = "http://10.0.2.2:5000/loginAPI"; // Hay que usar esta IP para referirnos a nuestra propia máquina y no al propio emulador

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

                try {
                    JSONObject json = new JSONObject(response.body().string());
                    final JSONObject data = json.getJSONObject("data");

                    if(data.getInt("error") == 1) {
                        identificado = false;

                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                // Mostramos alerta en login
                                TextView alerta = (TextView) findViewById(R.id.textView14);
                                alerta.setText("Datos incorrectos. Prueba de nuevo");
                            }
                        });
                    }

                    else if(data.getInt("error") == 0) {
                        identificado = true;
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                // Cambiamos la vista
                                setContentView(R.layout.perfil);

                                // Actualizamos el nombre del perfil
                                String user = null;
                                String emailUser = null;
                                int amigos = 0;
                                int seguidores = 0;

                                try {
                                    user = data.getString("user");
                                    emailUser = data.getString("email");
                                    amigos = data.getInt("cantidadAmigos");
                                    seguidores = data.getInt("cantidadSeguidores");

                                } catch (JSONException e) {
                                    e.printStackTrace();
                                }

                                // Nombre de usuario
                                TextView nombreUser = (TextView) findViewById(R.id.textView5) ;
                                nombreUser.setText(user);

                                // Ponemos el email de forma global para hacer la veces de sesión
                                email = emailUser;

                                // Número de amigos
                                TextView numAmigos = (TextView) findViewById(R.id.textView10);
                                numAmigos.setText(String.valueOf(amigos));

                                // Número de seguidores
                                TextView numSeguidores = (TextView) findViewById(R.id.textView11);
                                numSeguidores.setText(String.valueOf(seguidores));
                            }
                        });
                    }
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void cambiarNombre(View v) {
        String url = "http://10.0.2.2:5000/editProfileAPI"; // Hay que usar esta IP para referirnos a nuestra propia máquina y no al propio emulador

        final EditText name = (EditText) findViewById(R.id.editText);

        final OkHttpClient client = new OkHttpClient();

        RequestBody cuerpo = new FormBody.Builder()
                .add("email", email)
                .add("username", name.getText().toString())
                .build();

        final Request request = new Request.Builder()
                .url(url)
                .post(cuerpo)
                .build();

        if(identificado) {
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

                    try {
                        JSONObject json = new JSONObject(response.body().string());
                        final JSONObject respuesta = json.getJSONObject("respuesta");

                        if(respuesta.getInt("cambio") == 1) {
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    // Cambiamos de vista
                                    setContentView(R.layout.login);

                                    // Mostramos alerta para iniciar sesión de nuevo
                                    TextView alerta = (TextView) findViewById(R.id.textView14);
                                    alerta.setText("Nombre cambiado correctamente.\nInicia sesión de nuevo.");

                                    // Ya no estamos identificados
                                    identificado = false;
                                }
                            });
                        }

                        else if(respuesta.getInt("cambio") == 0) {
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    // Mostramos alerta de que no se ha podido cambiar el nombre
                                    TextView alertaPerfil = (TextView) findViewById(R.id.textView12);
                                    alertaPerfil.setText("No se ha podido cambiar tu nombre.\nPrueba de nuevo.");
                                }
                            });
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }

    public void mostrarPublicaciones(View v) {
        String url = "http://10.0.2.2:5000/publicacionesAPI"; // Hay que usar esta IP para referirnos a nuestra propia máquina y no al propio emulador

        final OkHttpClient client = new OkHttpClient();

        RequestBody cuerpo = new FormBody.Builder()
                .add("email", email)
                .build();

        final Request request = new Request.Builder()
                .url(url)
                .post(cuerpo)
                .build();

        if(identificado) {
            // Con .enqueue hacemos peticiones asíncronas
            // https://stackoverflow.com/questions/39440806/android-okhttpclient-requesting-error?rq=1
            client.newCall(request).enqueue(new Callback() {
                @Override
                public void onFailure(Call call, IOException e) {
                    e.printStackTrace();
                }

                @RequiresApi(api = Build.VERSION_CODES.KITKAT)
                @Override
                public void onResponse(Call call, final Response response) throws IOException {
                    if(!response.isSuccessful()) {
                        throw new IOException("Unexpected code " + response);
                    }

                    try {
                        final JSONObject json = new JSONObject(response.body().string());

                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                setContentView(R.layout.publicaciones);
                                TextView publicacionesJSON = (TextView) findViewById(R.id.publicacionesJSON);
                                publicacionesJSON.setText(json.toString());
                            }
                        });
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }
}