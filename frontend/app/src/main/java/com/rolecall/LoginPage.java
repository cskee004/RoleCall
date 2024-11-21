
package com.rolecall;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.example.rolecall.R;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import org.json.simple.JSONArray;

import org.json.simple.JSONObject;

import org.json.simple.parser.*;
import java.net.URLEncoder;



public class LoginPage extends AppCompatActivity {
    String enteredData;
    String enteredPassword;


    public String getEnteredPassword() {
        return enteredPassword;
    }

    public void setEnteredPassword(String enteredPassword) {
        this.enteredPassword = enteredPassword;
    }



    public String getEnteredData() {
        return enteredData;
    }

    public void setEnteredData(String enteredData) {
        this.enteredData = enteredData;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_login_page);
        EditText editText;
        EditText editPassword;
        EditText editEmail;
        Button submitButton;

        editText = (EditText) findViewById(R.id.editText);
        editPassword= (EditText)findViewById(R.id.editpassword);
        submitButton = (Button) findViewById(R.id.submitButton);


        submitButton.setOnClickListener(
                new View.OnClickListener() {
                    @Override
                    public void onClick(View view) {

                        setEnteredData(editText.getText().toString());
                        setEnteredPassword(editPassword.getText().toString());


                        Thread HttpThread= new  Thread(() -> {
                            try {

                                String urlString = "http://localhost:5000/login";
                                String username = "Berhans";
                                String password = "BEESecret";
                                JSONParser jsonParser = new JSONParser();


                                String encodedParams = "username=" + URLEncoder.encode(username, "UTF-8") +
                                        "&password=" + URLEncoder.encode(password, "UTF-8");

                                urlString+= "?"+encodedParams;
                                URL url = new URL(urlString);


                                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                                conn.setRequestMethod("GET");


                                int responseCode = conn.getResponseCode();
                                if (responseCode == 200) {

                                    BufferedReader in = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                                    String inputLine;
                                    StringBuilder content = new StringBuilder();

                                    while ((inputLine = in.readLine()) != null) {
                                        content.append(inputLine);
                                    }

                                    in.close();
                                    conn.disconnect();

                                    String holder = "";
                                    JSONParser parser = new JSONParser();
                                    JSONArray jsonResponse = (JSONArray) parser.parse(content.toString());
                                    for (Object element : jsonResponse) {
                                        // Each element is a JSONObject
                                        JSONObject jsonObject = (JSONObject) element;

                                        // Access individual fields in the JSONObject
                                        String name = (String) jsonObject.get("name");
                                        String SQLpassword = (String) jsonObject.get("password");
                                        holder=SQLpassword;

                                        System.out.println("Your Username: " + name + ", Your Password: " + SQLpassword);
                                    }


                                    if (holder == "") {
                                        System.out.println("Wrong login.");

                                    } else {
                                        System.out.println("Success");

                                    }


                                } else {
                                    System.out.println("Request failed with status: " + responseCode);
                                }
                            } catch (Exception e) {
                                e.printStackTrace();
                            }
                        });HttpThread.start();
                    }
                });

        Button mybutton = findViewById(R.id.nextButton);
        mybutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(view.getContext(), Profile.class);
                intent.putExtra("Username",enteredData);
                intent.putExtra("Password",enteredPassword);
                view.getContext().startActivity(intent);}
        });

        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
    }
}
