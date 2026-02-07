package main

import (
	"fmt"
	"net/http"
	"crypto/sha256"
	"encoding/hex"
	"time"
)

func challengeHandler(w http.ResponseWriter, r *http.Request) {
	// Simple cryptographic challenge: find a nonce such that sha256(timestamp + nonce) starts with "000"
	timestamp := time.Now().Unix()
	
	html := fmt.Sprintf(`
		<html>
		<head><title>Anubis AI Bot Blocker</title></head>
		<body>
			<h1>Security Challenge</h1>
			<p>Please wait while we verify your browser...</p>
			<script>
				const timestamp = "%d";
				function solve() {
					let nonce = 0;
					while (true) {
						const hash = btoa(timestamp + nonce); // Simplified for demo
						if (hash.startsWith("MDAw")) { // "000" in base64
							window.location.href = "/verify?nonce=" + nonce + "&ts=" + timestamp;
							break;
						}
						nonce++;
					}
				}
				setTimeout(solve, 1000);
			</script>
		</body>
		</html>
	`, timestamp)
	
	fmt.Fprintf(w, html)
}

func verifyHandler(w http.ResponseWriter, r *http.Request) {
	nonce := r.URL.Query().Get("nonce")
	ts := r.URL.Query().Get("ts")
	
	// In a real implementation, we would verify the hash here
	fmt.Fprintf(w, "Verification successful! Access granted for session %s-%s", ts, nonce)
}

func main() {
	http.HandleFunc("/", challengeHandler)
	http.HandleFunc("/verify", verifyHandler)
	fmt.Println("Anubis Bot Blocker running on port 9090...")
	http.ListenAndServe(":9090", nil)
}
