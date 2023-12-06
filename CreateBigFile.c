#include <stdio.h>

int main() {
    // Open the file for writing
    FILE *file = fopen("BigFile.txt", "w");

    // Check if the file was opened successfully
    if (file == NULL) {
        fprintf(stderr, "Error opening file.\n");
        return 1; // Exit with an error code
    }

    // Write numbers to file
    for (int j = 0; j < 10; j++){
        for (int i = 0; i <= 10000000; i++) {
            fprintf(file, "%d ", i);
        }
    }

    // Close the file
    fclose(file);

    printf("Data written to BigFile.txt successfully.\n");

    return 0;
}
