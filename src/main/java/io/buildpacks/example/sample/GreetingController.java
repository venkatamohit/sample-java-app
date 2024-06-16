package io.buildpacks.example.sample;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingController {

    @GetMapping("/greeting")
    public String greeting(@RequestParam(name="name", required=false, defaultValue="World") String name) {
        return "Hello, " + name + "!";
    }

    // New method that throws an exception
    @GetMapping("/error")
    public String throwError() {
        throw new RuntimeException("This is a deliberate error for PR review.");
    }
}
