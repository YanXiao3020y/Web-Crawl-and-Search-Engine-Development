### Project Overview:

-   **Goal**: Implement a complete search engine.

-   **Corpus**: A collection of ICS web pages (provided in a zip file).

-   **Main Challenges**: Full HTML parsing, file/database handling, and
    user input management.

### Milestone 1:

-   **Objective**: Build an index and a basic retrieval component.

-   **Tasks**:

    1.  **Create an Inverted Index**:

        -   Index all tokens from the HTML files.

        -   Remove stop words and apply lemmatization.

        -   Store additional metadata like TF-IDF scores and the
            importance of words in titles, bold, and heading tags.

    2.  **Basic Retrieval Component**:

        -   Implement a simple retrieval system that can query the index
            for single-word queries.

        -   Test with specific queries: \"Informatics,\" \"Mondego,\"
            \"Irvine.\"

-   **Data Collection**:

    1.  A table showing the number of documents, unique words, and total
        index size (in KB).

    2.  The number of URLs retrieved for each test query, listing the
        first 20 URLs.

### Milestone 2:

-   **Objective**: Complete the search engine.

-   **Tasks**:

    1.  Enhance the retrieval component to handle complex queries.

    2.  Implement ranking using TF-IDF and other mechanisms like
        PageRank, if desired.

### More Info
For additional details, please refer to the specification document provided as specification.pdf.