package com.example.hashtableservice.controller;

import com.example.hashtableservice.service.DictionaryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;

@RestController
@RequestMapping("/dictionary")
@CrossOrigin(origins = "http://localhost:8000") // Allow Django development server
public class DictionaryController {
    private final DictionaryService dictionaryService;

    public DictionaryController(DictionaryService dictionaryService) {
        this.dictionaryService = dictionaryService;
    }

    @GetMapping("/get")
    public ResponseEntity<String> get(  
            @RequestParam(required = true) String style,
            @RequestParam(required = true) String word) {
        try {
            if (style == null || style.trim().isEmpty() || word == null || word.trim().isEmpty()) {
                return ResponseEntity.badRequest().body("Style and word are required");
            }

            String definition = dictionaryService.getDefinition(style.trim(), word.trim());
            return ResponseEntity.ok(definition != null ? definition : "Definition not found");
        } catch (Exception e) {
            return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error retrieving definition: " + e.getMessage());
        }
    }

    @PostMapping("/add")
    public ResponseEntity<String> add(
            @RequestParam(required = true) String style,
            @RequestParam(required = true) String word,
            @RequestParam(required = true) String definition) {
        try {
            if (style == null || style.trim().isEmpty() 
                || word == null || word.trim().isEmpty()
                || definition == null || definition.trim().isEmpty()) {
                return ResponseEntity.badRequest().body("Style, word, and definition are required");
            }

            dictionaryService.putDefinition(style.trim(), word.trim(), definition.trim());
            dictionaryService.saveFile(); // Save after each addition
            return ResponseEntity.ok("Definition added successfully");
        } catch (Exception e) {
            return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error adding definition: " + e.getMessage());
        }
    }
}



