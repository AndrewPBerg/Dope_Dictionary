package com.example.hashtableservice.service;
import java.io.*;
import java.util.HashMap;
import org.springframework.stereotype.Service;

@Service
public class DictionaryService implements Serializable {
    private static final long serialVersionUID = 1L;
    private final HashMap<String, HashMap<String, String>> dictionary;
    private static final String STORAGE_FILE = "hashmap.ser";

    public DictionaryService() {
        this.dictionary = new HashMap<>();
        loadFile();
    }

    public String getDefinition(String style, String word) {
        HashMap<String, String> styleMap = this.dictionary.get(style);
        return styleMap != null ? styleMap.get(word) : null;
    }

    public void putDefinition(String style, String word, String definition) {
        HashMap<String, String> styleMap = this.dictionary.computeIfAbsent(style, k -> new HashMap<>());
        styleMap.put(word, definition);
    }

    public void saveFile() {
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(STORAGE_FILE))) {
            out.writeObject(this.dictionary);
        } catch (IOException e) {
            throw new RuntimeException("Failed to save dictionary", e);
        }
    }

    private void loadFile() {
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream(STORAGE_FILE))) {
            @SuppressWarnings("unchecked")
            HashMap<String, HashMap<String, String>> map = 
                (HashMap<String, HashMap<String, String>>) in.readObject();
            dictionary.clear();
            dictionary.putAll(map);
        } catch (IOException | ClassNotFoundException e) {
            // Start with empty dictionary if file cannot be loaded
        }
    }
}





