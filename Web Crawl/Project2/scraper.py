import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

crawled_url = set()
token_dict = {}
longest_words_page = ["", 0]    # get the url that has the longest word count, index0 is url, index1 is word count
subdomain_dict = {}
ban_list = ["evoke.ics.uci.edu/cory-knobel-receives-iconference-2014-best-paper-award",
            "evoke.ics.uci.edu/qs-personal-data-landscapes-poster"]
# Question 3: Open stop_words.txt and add all words into stopword_list
with open("stop_words.txt", "r", encoding='utf8', errors='ignore') as file:
    stop_list = file.read().split("\n")


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def tokenize(lst):
    new_list = []
    for token in lst:
        if token not in stop_list:  # Question 3: ignore english stop words
            matched_list = re.findall('[a-zA-Z]+', token) #
            for i in matched_list:
                if len(i) >= 2:
                    new_list.append(i)
    return new_list


def computeWordFrequencies(tokens):
    for token in tokens:
        if token in token_dict:
            token_dict[token] += 1
        else:
            token_dict[token] = 1
    return token_dict


def computeLocalFrequencies(tokens):
    local_dict = {}
    for token in tokens:
        if token in local_dict:
            local_dict[token] += 1
        else:
            local_dict[token] = 1
    return local_dict


def extract_next_links(url, resp):
    #use is_valid()
    #check resp.status == 200
    #check word_count
    # add url in crawled_url

    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    # Check if response status is 200
    if resp.status != 200 or not is_valid(url):
        return list()

    # Question 1: Discard the # part of the url
    fragment_position = url.find("#")
    if fragment_position != -1:
        url = url[:fragment_position]

    # Question 1: Avoid trap (third condition)
    if url in crawled_url:
        return list()

    # Adding to the crawling set
    crawled_url.add(url)

    # Count the number of unique urls and write into unique_url_num.txt
    with open("unique_url_num.txt", "w", encoding='utf8', errors='ignore') as file:
        file.write("There are " + str(len(crawled_url)) + " unique pages.")

    # Get the content of the page
    url_content = resp.raw_response.content

    # Parse the response content
    url_content_parse = BeautifulSoup(url_content, "lxml")

    # Get the content of the page, split the content into list of words
    not_token_list = url_content_parse.text.lower().split()

    # If the content of the url is under 20 words, skip the url (i.e page is 404 not found)
    # Example website: https://today.uci.edu/department/information_computer_sciences (15 word count)
    if len(not_token_list) < 20:
        return list()
    if "evoke" in url:
        return list()

    # if url contains evoke, crawl the top 100 reply
    '''if "evoke" in url:
        reply_count = 0
        reply_index = len(not_token_list)
        for i in range(len(not_token_list)):
            if not_token_list[i] == "Reply":
                reply_count += 1
            if reply_count == 1:
                reply_index = i
                break
        not_token_list = not_token_list[:reply_index]'''

    # Format the token
    content_token_list = tokenize(not_token_list)

    # Add the (global) word frequency into token dictionary
    global_token_dict = computeWordFrequencies(content_token_list)

    # Question 2: Add the (local) word frequency into token dictionary
    local_token_dict = computeLocalFrequencies(content_token_list)
    local_word_count = sum(list(local_token_dict.values())) # Q2: The Longest word count
    if local_word_count > longest_words_page[1]:
        longest_words_page[0] = url
        longest_words_page[1] = local_word_count

    # Question 2: Place the longest word count into largest_word_count.txt
    with open("largest_word_count.txt", "w", encoding='utf8', errors='ignore') as file:
        file.write(str(longest_words_page))

    # Question 3: Add frequency dictionary to fifty_most_words.txt
    with open("fifty_most_words.txt", "w", encoding='utf8', errors='ignore') as file:
        count = 0
        for key, value in sorted(token_dict.items(), key=lambda x: x[1], reverse=True):
            word_str = key + ": " + str(value) + "\n" #  "\n" format
            file.write(word_str)
            count += 1
            if count == 50:
                break

    link_lst = []   # find url list that starts with href
    for i in url_content_parse.find_all("a"):
        not_format_url = i.get('href')
        # Remove slash ("/") from url
        if not_format_url is not None:
            if "/" in not_format_url and not_format_url[-1] == "/":
                format_url = not_format_url[:-1]
                link_lst.append(format_url)
            else:
                link_lst.append(not_format_url)

    # Question 1: Store url into file
    with open("URLs.txt", 'w', encoding='utf-8', errors='ignore') as file:
        for i in crawled_url:
            file.write(i + "\n")

    # Question 4: Find subdomain
    parse = urlparse(url)
    net = parse.netloc
    if "ics.uci.edu" in net:
        if net in subdomain_dict.keys():
            subdomain_dict[net] += 1
        else:
            subdomain_dict[net] = 1

    # put subdomain dictionary into subdomain.txt
    with open("subdomain.txt", 'w', encoding='utf-8', errors='ignore') as file:
        for key, value in sorted(subdomain_dict.items()):
            file.write(key + ", " + str(value) + "\n")
    return link_lst


def is_domain(url):
    parse = urlparse(url)
    net = parse.netloc
    domain = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu"]
    if "today.uci.edu/department/information_computer_sciences" in net + parse.path:
        return True
    for i in domain:
        if i in net:
            return True
    return False


def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        # Return false if url is empty
        if url == "" or url is None:
            return False

        # Check if the url has already crawled
        if url in crawled_url:
            return False

        # Check if the url is within our domain
        if not is_domain(url):
            return False

        # Parse url to check the format
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise




