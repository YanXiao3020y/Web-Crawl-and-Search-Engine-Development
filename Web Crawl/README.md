The project involves implementing a web crawler using Python,
specifically utilizing the crawler4j or crawler4py libraries. The main
goal is to crawl the domain ics.uci.edu, adhering to specific guidelines
like setting the User Agent and respecting a 300ms delay between
requests to the same subdomain. The crawler should focus only on
ics.uci.edu and its subdomains, storing the crawled pages for further
analysis.

### Key Tasks:

1.  **Crawling the Domain**: Start from the seed http://www.ics.uci.edu
    and crawl only within the domain and its subdomains.

2.  **Data Collection**:

    -   Time taken to crawl the entire domain.

    -   Number of unique pages found (based on URL).

    -   List of subdomains found, with the count of unique pages in
        each.

    -   The longest page by word count (excluding HTML markup).

    -   The 500 most common words, excluding English stop words.

    -   The 20 most common 3-grams, also excluding stop words.

### More Info
For additional details, please refer to the specification document provided as specification.pdf.