package main

import (
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

// TestBuildPrompt verifica que la función BuildPrompt genere correctamente
// las instrucciones de resumen según el tipo solicitado.
func TestBuildPrompt(t *testing.T) {
	text := "Artificial intelligence is transforming industries worldwide."

	tests := []struct {
		name     string
		typ      string
		expected string
	}{
		{"Short summary", "short", "1-2 concise sentences"},
		{"Medium summary", "medium", "one paragraph"},
		{"Bullet summary", "bullet", "list of bullet points"},
		{"Default summary", "unknown", "Summarize the following text"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			prompt := BuildPrompt(tt.typ, text)
			if !strings.Contains(prompt, tt.expected) {
				t.Errorf("BuildPrompt(%s) = %q; no contiene %q", tt.typ, prompt, tt.expected)
			}
			if !strings.Contains(prompt, text) {
				t.Errorf("El texto original no fue incluido en el prompt generado")
			}
		})
	}
}

// TestInitLogger valida que el logger se inicialice correctamente
// y cree el archivo de log esperado en el directorio logs/.
func TestInitLogger(t *testing.T) {
	logDir := "logs"
	logFile := filepath.Join(logDir, "app.log")

	// Elimina logs previos si existen
	os.RemoveAll(logDir)

	InitLogger()

	// Verifica que el logger esté definido
	if Logger == nil {
		t.Fatalf("Logger no fue inicializado")
	}

	// Verifica que el archivo se haya creado
	if _, err := os.Stat(logFile); os.IsNotExist(err) {
		t.Fatalf("El archivo de log no fue creado en %s", logFile)
	}

	// Limpieza al finalizar
	os.RemoveAll(logDir)
}

// TestRequestPayloadStructure valida que la estructura RequestPayload
// se serialice correctamente a JSON.
func TestRequestPayloadStructure(t *testing.T) {
	payload := RequestPayload{
		Inputs: "Summarize this text",
		Parameters: map[string]interface{}{
			"max_length": 60,
			"min_length": 20,
		},
	}

	data, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("Error serializando RequestPayload: %v", err)
	}

	jsonStr := string(data)
	if !strings.Contains(jsonStr, "Summarize this text") {
		t.Errorf("El JSON resultante no contiene el texto original")
	}
	if !strings.Contains(jsonStr, "max_length") {
		t.Errorf("El JSON resultante no contiene los parámetros esperados")
	}
}
