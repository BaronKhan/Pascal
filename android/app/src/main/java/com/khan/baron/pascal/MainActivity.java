package com.khan.baron.pascal;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.speech.RecognizerIntent;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.jcraft.jsch.ChannelExec;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.Session;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainActivity extends AppCompatActivity {
    private TextView txtSpeechInput;
    private TextView txtSpeechOutput;
    private TextView txtSpeechInstruction;
    private final int REQ_CODE_SPEECH_INPUT = 100;
    private String outputText = "";

    private Runnable runnable;

    private Handler handler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        txtSpeechInput = (TextView) findViewById(R.id.txtSpeechInput);
        txtSpeechOutput = (TextView) findViewById(R.id.txtSpeechOutput);
        txtSpeechInstruction = (TextView) findViewById(R.id.txtSpeechInstruction);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Voice request in progress...", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
                promptSpeechInput();
                txtSpeechInstruction.setText("");
            }
        });

        runnable = new Runnable() {
            @Override
            public void run() {
                onSpeechOutputUpdate();
                handler.postDelayed(this, 100);
            }
        };
        handler = new Handler();
        handler.postDelayed(runnable, 100);
    }

    private void promptSpeechInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        try {
            startActivityForResult(intent, REQ_CODE_SPEECH_INPUT);
        } catch (ActivityNotFoundException a) {
            Toast.makeText(getApplicationContext(),
                    getString(R.string.speech_not_supported),
                    Toast.LENGTH_SHORT).show();
        }
    }

    private void executeCommand(String command)  {
        final String my_command = command;
        outputText = "Waiting for response...";
        new AsyncTask<Integer, Void, Void>(){
            @Override
            protected Void doInBackground(Integer... params) {
                Session session = null;
                ChannelExec channel = null;
                try {
                    JSch jsch = new JSch();
                    JSch.setConfig("StrictHostKeyChecking", "no");

                    session = jsch.getSession("pi", "192.168.1.232", 22);
                    session.setPassword("mypiowhy");
                    session.connect();

                    channel = (ChannelExec)session.openChannel("exec");
                    InputStream in = channel.getInputStream();
                    channel.setErrStream(System.err);
                    channel.setCommand("python3 Pascal/main.py --text '"+my_command+"'");
                    channel.connect();

                    StringBuilder message = new StringBuilder();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(in));
                    String line = null;
                    while ((line = reader.readLine()) != null)
                    {
                        message.append(line).append("\n");
                    }
                    channel.disconnect();
                    while (!channel.isClosed()) {

                    }
                    System.out.println("Exit status: "+channel.getExitStatus());
                    System.out.println("Message: "+message.toString());
                    String pattern = "\\|(.*)\\|";

                    Pattern r = Pattern.compile(pattern);

                    Matcher m = r.matcher(message.toString());
                    if (m.find( )) {
                        outputText = m.group(0).replaceAll("\\|", "");

                    }else {
                        outputText = "Error: no response from Pascal";
                    }

                    System.out.println(outputText);

                } catch (Exception e) {
                    e.printStackTrace();
                    outputText = "Error: could not connect to Pascal";
                    System.out.println(outputText);
                }
                return null;
            }
        }.execute(1);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        switch (requestCode) {
            case REQ_CODE_SPEECH_INPUT: {
                if (resultCode == RESULT_OK && null != data) {

                    ArrayList<String> result = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
                    txtSpeechInput.setText(result.get(0));
                    executeCommand(result.get(0));
                }
                break;
            }

        }
    }

    protected void onSpeechOutputUpdate() {
        txtSpeechOutput.setText(outputText);
    }
}
