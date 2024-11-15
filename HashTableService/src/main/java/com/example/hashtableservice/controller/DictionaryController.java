package com.example.hashtableservice.controller;

import com.example.hashtableservice.service.DictionaryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
//need error handling

@RestController
@RequestMapping("/dictionary")
public class DictionaryController {
    private final DictionaryService dictionaryService = new DictionaryService();

    @GetMapping("/get") //*this allows django backend to get definition from microservice (hashmap)
    public ResponseEntity<String> get( //*parameters and method depends on what jason makes them
            @RequestParam String style,
            @RequestParam String word) {
        String definition = dictionaryService.get(style, word);

        if (definition != null) {
            return ResponseEntity.ok(definition);
        } else {
            return ResponseEntity.ok("Definition not found");
        }

    }

    @PostMapping("/add") //*this is what allows Gemini to add new definition to hashmap
    public ResponseEntity<String> add( //*this depends again on how jason makes them
            @RequestParam String style,
            @RequestParam String word,
            @RequestParam String definition) {

        dictionaryService.add();
        return ResponseEntity.ok("Definition added");
    }
}



