package com.rolecall;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.example.rolecall.R;

import java.util.HashMap;

public class ViewListing extends AppCompatActivity {
    private Listing display;
    private String userId;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_view_listing);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        Intent intent = getIntent();
        display = (Listing) intent.getSerializableExtra("Listing");
        userId = (String) intent.getExtras().get("userId");
        fillFields(new TextView(this));
    }

    public void backToListings(View v){
        finish();
    }

    public void findMatches(View v){
        Intent intent = new Intent(ViewListing.this, MatchingListings.class);
        intent.putExtra("listingId", display.getListingId());
        intent.putExtra("userId", userId);
        startActivity(intent);
    }

    public void editListing(View v){
        Intent intent = new Intent(ViewListing.this, EditListingsPage.class);
        intent.putExtra("listing", display);
        startActivity(intent);
    }

    public void fillFields(View v){
        //Implemented Logic
        TextView gameName = findViewById(R.id.game_name_field);
        TextView difficulty = findViewById(R.id.difficulty_field);
        TextView environment = findViewById(R.id.environment_field);
        TextView day = findViewById(R.id.day_field);
        TextView startTime = findViewById(R.id.start_time_field);
        TextView endTime = findViewById(R.id.end_time_field);
        TextView role = findViewById(R.id.role_field);
        gameName.setText(display.getGameName());
        difficulty.setText(display.getDifficulty());
        environment.setText(display.getEnvironment());
        day.setText(display.getDay());
        startTime.setText(display.getStartTime());
        endTime.setText(display.getEndTime());
        role.setText(display.getRole().toString());
    }
}