package downloader

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
)

// Config holds configuration settings for the downloader
type Config struct {
	Concurrency   int           // Number of concurrent downloads
	Timeout       time.Duration // Timeout for each download
	OutputDir     string        // Directory to save downloaded images
	SkipExisting  bool          // Whether to skip existing files
	Verbose       bool          // Whether to print verbose output
}

// DefaultConfig returns a default configuration
func DefaultConfig() Config {
	return Config{
		Concurrency:  5,
		Timeout:      30 * time.Second,
		OutputDir:    "./downloads",
		SkipExisting: true,
		Verbose:      true,
	}
}

// DownloadResult represents the result of a download operation
type DownloadResult struct {
	URL      string // Source URL
	FilePath string // Where the file was saved
	Success  bool   // Whether the download was successful
	Error    error  // Error if any
}

// DownloadImages downloads a list of image URLs to the specified directory
func DownloadImages(urls []string, config Config) []DownloadResult {
	// Create output directory if it doesn't exist
	if err := os.MkdirAll(config.OutputDir, 0755); err != nil {
		fmt.Printf("Error creating output directory: %v\n", err)
		return []DownloadResult{{Success: false, Error: err}}
	}

	// Create a semaphore to limit concurrency
	semaphore := make(chan struct{}, config.Concurrency)
	var wg sync.WaitGroup
	results := make([]DownloadResult, len(urls))

	// Create context with timeout
	ctx, cancel := context.WithTimeout(context.Background(), config.Timeout*time.Duration(len(urls)/config.Concurrency+1))
	defer cancel()

	// Process each URL
	for i, url := range urls {
		wg.Add(1)
		go func(i int, url string) {
			defer wg.Done()

			// Acquire semaphore
			semaphore <- struct{}{}
			defer func() { <-semaphore }()

			// Skip empty URLs
			if url == "" {
				results[i] = DownloadResult{URL: url, Success: false, Error: fmt.Errorf("empty URL")}
				return
			}

			// Get filename from URL
			fileName := getFileNameFromURL(url)
			filePath := filepath.Join(config.OutputDir, fileName)

			// Check if file already exists
			if config.SkipExisting {
				if _, err := os.Stat(filePath); err == nil {
					if config.Verbose {
						fmt.Printf("Skipping %s: file already exists\n", fileName)
					}
					results[i] = DownloadResult{URL: url, FilePath: filePath, Success: true}
					return
				}
			}

			// Download the file
			result := downloadFile(ctx, url, filePath, config.Verbose)
			results[i] = result

		}(i, url)
	}

	// Wait for all downloads to complete
	wg.Wait()
	return results
}

// downloadFile downloads a single file from a URL to the specified path
func downloadFile(ctx context.Context, url string, filePath string, verbose bool) DownloadResult {
	result := DownloadResult{
		URL:      url,
		FilePath: filePath,
	}

	// Create HTTP request
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		result.Success = false
		result.Error = fmt.Errorf("error creating request: %w", err)
		if verbose {
			fmt.Printf("Error downloading %s: %v\n", url, err)
		}
		return result
	}

	// Add appropriate headers
	req.Header.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")

	// Send the request
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		result.Success = false
		result.Error = fmt.Errorf("error sending request: %w", err)
		if verbose {
			fmt.Printf("Error downloading %s: %v\n", url, err)
		}
		return result
	}
	defer resp.Body.Close()

	// Check if the request was successful
	if resp.StatusCode != http.StatusOK {
		result.Success = false
		result.Error = fmt.Errorf("received non-200 status code: %d", resp.StatusCode)
		if verbose {
			fmt.Printf("Error downloading %s: received status code %d\n", url, resp.StatusCode)
		}
		return result
	}

	// Create the output file
	out, err := os.Create(filePath)
	if err != nil {
		result.Success = false
		result.Error = fmt.Errorf("error creating file: %w", err)
		if verbose {
			fmt.Printf("Error creating file %s: %v\n", filePath, err)
		}
		return result
	}
	defer out.Close()

	// Copy the response body to the output file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		result.Success = false
		result.Error = fmt.Errorf("error writing to file: %w", err)
		if verbose {
			fmt.Printf("Error writing to file %s: %v\n", filePath, err)
		}
		return result
	}

	result.Success = true
	if verbose {
		fmt.Printf("Successfully downloaded %s to %s\n", url, filePath)
	}
	return result
}

// getFileNameFromURL extracts the filename from a URL
func getFileNameFromURL(url string) string {
	// Extract the base name from the URL
	parts := strings.Split(url, "/")
	if len(parts) == 0 {
		return "unknown.jpg"
	}
	fileName := parts[len(parts)-1]

	// Remove query parameters
	if idx := strings.IndexByte(fileName, '?'); idx >= 0 {
		fileName = fileName[:idx]
	}

	// If no extension, add .jpg
	if !strings.Contains(fileName, ".") {
		fileName += ".jpg"
	}

	return fileName
}

// DownloadFromURLs is a simplified function to download images to a specific folder
func DownloadFromURLs(urls []string, outputDir string) []DownloadResult {
	config := DefaultConfig()
	config.OutputDir = outputDir
	return DownloadImages(urls, config)
}
