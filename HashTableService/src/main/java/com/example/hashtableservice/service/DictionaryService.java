package com.example.hashtableservice.service;
import java.io.*;
import java.util.HashMap;
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class DictionaryService implements Serializable {
    private static final long serialVersionUID = 1L;
    private static final Logger logger = LoggerFactory.getLogger(DictionaryService.class);
    private final HashMap<String, HashMap<String, String>> dictionary;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    private static final String STORAGE_FILE = "hashmap.ser";

    public DictionaryService() {
        this.dictionary = new HashMap<>();
        loadFile();
    }

    public String getDefinition(String style, String word) {
        lock.readLock().lock();
        try {
            HashMap<String, String> styleMap = this.dictionary.get(style);
            return styleMap != null ? styleMap.get(word) : null;
        } finally {
            lock.readLock().unlock();
        }
    }

    public void putDefinition(String style, String word, String definition) {
        lock.writeLock().lock();
        try {
            HashMap<String, String> styleMap = this.dictionary.computeIfAbsent(style, k -> new HashMap<>());
            styleMap.put(word, definition);
        } finally {
            lock.writeLock().unlock();
        }
    }

    public void saveFile() {
        lock.writeLock().lock();
        try (ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(STORAGE_FILE))) {
            out.writeObject(this.dictionary);
            logger.info("Dictionary saved successfully");
        } catch (IOException e) {
            logger.error("Error saving dictionary: " + e.getMessage(), e);
            throw new RuntimeException("Failed to save dictionary", e);
        } finally {
            lock.writeLock().unlock();
        }
    }

    private void loadFile() {
        lock.writeLock().lock();
        try (ObjectInputStream in = new ObjectInputStream(new FileInputStream(STORAGE_FILE))) {
            @SuppressWarnings("unchecked")
            HashMap<String, HashMap<String, String>> map = 
                (HashMap<String, HashMap<String, String>>) in.readObject();
            dictionary.clear();
            dictionary.putAll(map);
            logger.info("Dictionary loaded successfully");
        } catch (IOException | ClassNotFoundException e) {
            logger.warn("Could not load dictionary file, starting with empty dictionary: " + e.getMessage());
        } finally {
            lock.writeLock().unlock();
        }
    }
}







