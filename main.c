#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libxml/parser.h>
#include <libxml/tree.h>

void validateXmlFile(const char *xmlFileName) {
    xmlDocPtr doc = xmlReadFile(xmlFileName, NULL, 0);

    if (doc == NULL) {
        fprintf(stderr, "Error: Unable to parse XML file '%s'\n", xmlFileName);
        printf("\n");
    }
    
    else {
        printf("XML file '%s' is syntactically valid.\n", xmlFileName);
        printf("\n");
        // Free the resources allocated by libxml2
        xmlFreeDoc(doc);
    }
}

int main() {
    // Initialize the libxml2 library
    LIBXML_TEST_VERSION;

    // Iterate through the generated XML files in generated_xmls
    for (int fileNumber = 1; fileNumber <= 5; ++fileNumber) {
        char xmlFileName[50];
        snprintf(xmlFileName, sizeof(xmlFileName), "generated_xmls/generated_file_%d.xml", fileNumber);

        // Validate each XML file
        validateXmlFile(xmlFileName);
    }

    // Cleanup libxml2
    xmlCleanupParser();

    return 0;
}

/*
Run the following to compile and execute the parser program (main.c):
gcc -o main main.c -lxml2
./main generated_xmls/generated_file_1.xml generated_xmls/generated_file_2.xml generated_xmls/generated_file_3.xml generated_xmls/generated_file_4.xml generated_xmls/generated_file_5.xml
*/