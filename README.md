# url-shortner
simple url-shortner to learn more about system design

#### What is an url shortner
A program that reduces the length of an URL without losing it's properties. Used mainly for sharing and storing URL's that are big. Storage benefits, used in instant messaging services (messenger, twitter etc.) as there is a cap on how many characters a message can carry. Can also be used for malicious work, as the tiny URL often hides the redirect.

#### How does it work
The client calls the domain of a server with a path parameter. That path parameter is an ID associated with the original link. The ID can be anything, but often randomly generated, hashed or using auto-increment indexes and converting them to base36/32  The ID is case-sensitive and often in base 36 (26 characters + 10 numbers) or base 62 if we also want to include capital letters. 

#### How I think it's built
What it's composed of: 
* A backend server
	* handles logic, exposes two endpoints: `/generate`, `/URL_ID` where the URL_ID can be any ID's generated.
		* `/generate` POST request, takes a path/query paramater or a Form Data body with the original url, return URL_ID either from DB(already existing) or by generating it. 
		* `/URL_ID` GET request, fetches ORIGINAL_URL from DB and returns a 302 response with the ORIGINAL_URL in the response header. returns 404 if ORIGINAL_URL not found, i.e if ID is incorrect.
* DB
	* Stores a mapping between ID's and original URL's. 

###### URL_ID generation: 
**Random generation:** URL_ID has a fixed length. This length decides how many unique url's we can encode.  Let $u \in URL\_IDs$ be an arbitary url_id and $|u|$ define the length of it. Let $b$ define the number of unique values a character can take, $b=36$ for example. Then: $$|URL\_IDs|=b^{|u|}$$
so for example: if $|u|=3$ and $b=36$ $|URL\_IDs| = 36^3 = 46656$. That's 46656 unique URLs. There are around 200 million 'active' websites around there. To encode them all, length of $u$ would have to be $36^x=2 * 10^8 \rightarrow x =log_{36}(2*10^8)=5.33$. [TinyUrl](https://tinyurl.com/)uses and ID of 8 letters also with base 36 I think. That's $36^8=2.82*10^{12}$ which is almost 3 trillion. The number of registered URL's is about 4 billion. The ID space must be large enough for the number of shortened links stored in our database, not the number of websites on the internet. Multiple shortened links can point to the same destination URL, and one website can contain many URLs.

Let $n$ be the total number of IDs currently stored in DB and $N$ be the total space we afford (number of rows basically). The probability of generating an ID that is already among those in DB is $$\frac{n}{N}$$. The probability of generating a valid ID is $$1-\frac{n}{N}$$. And the number of expected generations for a valid ID is $$\frac{1}{1-\frac{n}{N}}$$. This is coming from the [geometric distribution](https://www.geeksforgeeks.org/maths/geometric-distribution/) (how many attempts before succees). 
Example: $n=3*10^9$ and $N=2.82*10^{12}$ then the expected number of generations for a valid ID is  $1.001$ xD, so time complexity is O(1). If we index the entries in DB, **retrieval** time becomes $O(log(n))$ because the index data structure is a B-tree, and $O(n)$ without indexing. **Storage** is $O(n)$. 

**Base36/62 conversion:** URL_ID is the base32 of it's index which is an auto-increment integer. Pros: No colissions, fast, easy to implement. Cons: IDs are predictable, easy to guess, length id depends on the index number. 
#### System design: 
* **Relevant Metrics:** number of users, number of requests, number of concurrent requests.
* **Components:** Number of servers, Number of app instances, number of DB's, Number of load balancers.
* **Techniques to optimize storage and retrieval time**: Set an expiration time on the ID. Use Redis for cache (Redis is an in-memory DB) and Postgres for storage. Flag relevant URL's and put them in Redis (hot URLs). Database sharding strategy for URL mappings (range vs hash-based). how to handle high-read write ratios and potential collisions.