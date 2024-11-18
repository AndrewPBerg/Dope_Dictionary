package com.example.hashtableservice.controller;

import com.example.hashtableservice.service.DictionaryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
//need error handling

@RestController
@RequestMapping("/dictionary")
public class DictionaryController {
    private final DictionaryService dictionaryService = new DictionaryService();

    @GetMapping("/get")
    public ResponseEntity<String> get(
            @RequestParam String style,
            @RequestParam String word) {
        String definition = dictionaryService.getDefinition(style, word);

        if (definition != null) {
            return ResponseEntity.ok(definition);
        } else {
            return ResponseEntity.ok("Definition not found");
        }
    }

    @PostMapping("/add")
    public ResponseEntity<String> add(
            @RequestParam String style,
            @RequestParam String word,
            @RequestParam String definition) {

        dictionaryService.putDefinition(style, word, definition);
        return ResponseEntity.ok("Definition added");
    }
}



