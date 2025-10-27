/*
solution_summarizer.go
-----------------------
CLI para resumir el contenido de un archivo de texto usando un modelo público de GenAI (HuggingFace Inference API).

Autor: Sergio Ignacio Posso Alvarez
Go Version: go1.25.3 windows/amd64

Objetivo:
- Leer un archivo de texto local.
- Enviar su contenido a una API pública de resumen (modelo HuggingFace).
- Mostrar el resultado en consola según el tipo de resumen solicitado.

Parámetros:
--input o argumento posicional : Ruta del archivo de texto.
--type  o -t                  : Tipo de resumen. Opciones: short | medium | bullet

Ejemplos de ejecución:
    go run solution_summarizer.go --input article.txt --type bullet
    go run solution_summarizer.go -t short article.txt

Tipos de resumen:
- short  → Resumen conciso (1-2 frases)
- medium → Párrafo descriptivo
- bullet → Lista de puntos clave

API usada:
Modelo: facebook/bart-large-cnn (Requiere un token de la variable de entorno HUGGINGFACE_TOKEN)
Referencia de API: https://huggingface.co/docs/api-inference/detailed_parameters#summarization
Endpoint público: https://api-inference.huggingface.co/models/facebook/bart-large-cnn

Manejo de errores:
- Valida argumentos obligatorios.
- Controla errores de red y respuestas inválidas.
- Implementa la mejor práctica de seguridad leyendo el token de HUGGINGFACE_TOKEN.
- Muestra mensajes legibles al usuario.
- Genera trazabilidad completa en el log local (logs/app.log).
*/

package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

// ===== LOGGER =====
var Logger *log.Logger

func InitLogger() {
	logDir := filepath.Join("logs")
	if _, err := os.Stat(logDir); os.IsNotExist(err) {
		os.MkdirAll(logDir, os.ModePerm)
	}

	logFile := filepath.Join(logDir, "app.log")
	file, err := os.OpenFile(logFile, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("Error al crear archivo de log: %v", err)
	}

	Logger = log.New(file, "[GoSummarizer] ", log.Ldate|log.Ltime|log.Lshortfile)
	Logger.Println("Logger inicializado correctamente.")
}

// ===== ESTRUCTURAS =====
type RequestPayload struct {
	Inputs     string                 `json:"inputs"`
	Parameters map[string]interface{} `json:"parameters,omitempty"`
}

type ResponsePayload []struct {
	SummaryText string `json:"summary_text"`
}

// ===== FUNCIONES =====
func BuildPrompt(summaryType string, text string) string {
	switch summaryType {
	case "short":
		return "Summarize the following text in 1-2 concise sentences:\n\n" + text
	case "medium":
		return "Provide a medium-length summary (one paragraph) of the following text:\n\n" + text
	case "bullet":
		return "Summarize the following text as a list of bullet points:\n\n" + text
	default:
		return "Summarize the following text:\n\n" + text
	}
}

// ===== MAIN =====
func main() {
	InitLogger()
	Logger.Println("Inicio de ejecución del CLI Summarizer")

	inputPath := flag.String("input", "", "Ruta del archivo de texto a resumir")
	summaryType := flag.String("type", "short", "Tipo de resumen: short | medium | bullet")
	flag.StringVar(summaryType, "t", "short", "Alias de --type")
	flag.Parse()

	if *inputPath == "" && flag.NArg() > 0 {
		*inputPath = flag.Arg(0)
	}

	// Validar tipo de resumen permitido
	validTypes := map[string]bool{"short": true, "medium": true, "bullet": true}
	if !validTypes[*summaryType] {
		fmt.Printf("Error: Tipo de resumen inválido: '%s'\n", *summaryType)
		fmt.Println("Valores válidos: short | medium | bullet")
		Logger.Printf("Error: Tipo de resumen inválido recibido: %s", *summaryType)
		os.Exit(1)
	}

	if *inputPath == "" {
		fmt.Println("Error: Debes especificar un archivo de entrada con --input o como argumento posicional.")
		Logger.Println("Error: No se especificó archivo de entrada.")
		os.Exit(1)
	}

	const envVarName = "HUGGINGFACE_TOKEN"
	huggingFaceToken := os.Getenv(envVarName)
	if huggingFaceToken == "" {
		fmt.Printf("Error (Seguridad): La API de HuggingFace requiere un token de autenticación.\n")
		fmt.Printf("Define la variable de entorno %s. Ejemplo:\n", envVarName)
		fmt.Printf("PowerShell: $env:%s=\"tu_token\"\n", envVarName)
		os.Exit(1)
	}

	content, err := os.ReadFile(*inputPath)
	if err != nil {
		Logger.Printf("Error al leer el archivo: %v", err)
		fmt.Printf("Error al leer el archivo: %v\n", err)
		os.Exit(1)
	}

	text := strings.TrimSpace(string(content))
	if len(text) == 0 {
		Logger.Println("Error: El archivo está vacío.")
		fmt.Println("Error: El archivo está vacío.")
		os.Exit(1)
	}

	// Validación adicional: tamaño máximo del texto (previene errores del modelo)
	if len(text) > 10000 {
		Logger.Printf("Advertencia: El archivo supera los 10,000 caracteres (%d). Podría truncarse el resumen.", len(text))
		fmt.Println("Advertencia: El texto es extenso. El modelo podría truncar el resultado.")
	}

	// Parámetros según tipo
	var params map[string]interface{}
	switch *summaryType {
	case "short":
		params = map[string]interface{}{"max_length": 60, "min_length": 20}
	case "medium":
		params = map[string]interface{}{"max_length": 150, "min_length": 80}
	case "bullet":
		params = map[string]interface{}{"max_length": 250, "min_length": 50}
	default:
		params = map[string]interface{}{}
	}

	prompt := BuildPrompt(*summaryType, text)
	payload := RequestPayload{Inputs: prompt, Parameters: params}

	apiURL := "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
	body, err := json.Marshal(payload)
	if err != nil {
		Logger.Printf("Error al serializar payload: %v", err)
		os.Exit(1)
	}

	client := &http.Client{Timeout: 60 * time.Second}
	req, err := http.NewRequest("POST", apiURL, bytes.NewBuffer(body))
	if err != nil {
		Logger.Printf("Error creando solicitud: %v", err)
		os.Exit(1)
	}

	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer "+huggingFaceToken)
	req.Header.Set("User-Agent", "GoCLI-Summarizer-App")

	fmt.Println("Enviando solicitud a HuggingFace ...")
	Logger.Printf("Enviando solicitud a HuggingFace | Modelo: facebook/bart-large-cnn | Tipo: %s", *summaryType)

	resp, err := client.Do(req)
	if err != nil {
		Logger.Printf("Error de red: %v", err)
		fmt.Printf("Error de red al contactar la API: %v\n", err)
		os.Exit(1)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		Logger.Printf("Error de API (%d): %s", resp.StatusCode, string(bodyBytes))
		fmt.Printf("Error de API (%d): %s\n", resp.StatusCode, string(bodyBytes))
		os.Exit(1)
	}

	var response ResponsePayload
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		Logger.Printf("Error al decodificar JSON: %v", err)
		fmt.Printf("Error al procesar la respuesta (JSON inválido): %v\n", err)
		os.Exit(1)
	}

	if len(response) > 0 && response[0].SummaryText != "" {
		summary := strings.TrimSpace(response[0].SummaryText)
		fmt.Println("\nResumen generado:\n------------------")
		Logger.Printf("Resumen generado correctamente. Longitud: %d caracteres", len(summary))
		Logger.Printf("Primeras palabras: %.80s", summary)

		if *summaryType == "bullet" && !strings.Contains(summary, "\n-") {
			formatted := strings.ReplaceAll(summary, ". ", ".\n- ")
			if strings.HasPrefix(formatted, "- ") {
				fmt.Println(formatted)
			} else {
				fmt.Println("- " + formatted)
			}
		} else {
			fmt.Println(summary)
		}
	} else {
		fmt.Println("No se recibió un resumen válido o el resumen está vacío.")
		Logger.Println("No se recibió un resumen válido.")
	}
}
