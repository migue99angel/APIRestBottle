package com.example.p4ds;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.sql.*;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

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

        Button btn = (Button) findViewById(R.id.button);
        btn.setOnClickListener(new View.OnClickListener() {
            @RequiresApi(api = Build.VERSION_CODES.KITKAT)
            @Override
            public void onClick(View v) {
                iniciarSesion(v);
                setContentView(R.layout.perfil);
            }
        });
    }

    @RequiresApi(api = Build.VERSION_CODES.KITKAT)
    public void iniciarSesion(View view) {
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

                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            // Actualizamos el nombre del perfil
                            String user = null;
                            try {
                                user = data.getString("user");
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                            TextView nombreUser = (TextView) findViewById(R.id.textView5) ;
                            nombreUser.setText(user);
                        }
                    });
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }
}