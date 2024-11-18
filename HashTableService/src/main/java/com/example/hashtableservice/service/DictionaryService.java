package com.example.hashtableservice.service;
import java.io.*;
import java.util.HashMap;

public class DictionaryService {
    public HashMap<String, HashMap<String, String>> dictionary;

    public DictionaryService() {
        this.dictionary = new HashMap<>();
        try {
            loadFile();
        } catch (Exception e) {
            this.dictionary = new HashMap<>();
        }
    }

    public String getDefinition(String style, String word) {
        HashMap<String, String> styleMap = this.dictionary.get(style);
        if (styleMap == null) {
            return null;
        }
        return styleMap.get(word);
    }

    public void putDefinition(String style, String word, String definition) {
        HashMap<String, String> styleMap = this.dictionary.computeIfAbsent(style, k -> new HashMap<>());
        styleMap.put(word, definition);
    }

    public void saveFile() {
        try (FileOutputStream fileOut = new FileOutputStream("hashmap.ser");
             ObjectOutputStream out = new ObjectOutputStream(fileOut)) {
            out.writeObject(this.dictionary);
            System.out.println("HashMap serialized to hashmap.ser");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void loadFile() {
        try (FileInputStream fileIn = new FileInputStream("hashmap.ser");
             ObjectInputStream in = new ObjectInputStream(fileIn)) {
            @SuppressWarnings("unchecked")
            HashMap<String, HashMap<String, String>> map = 
                (HashMap<String, HashMap<String, String>>) in.readObject();
            System.out.println("HashMap deserialized from hashmap.ser");
            this.dictionary = map;
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}







