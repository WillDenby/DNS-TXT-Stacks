# DNS-TXT-Stacks
Extracting, Cleaning, and Presenting the DNS TXT Records of the Top 1000 Sites

My first non-trivial coding project!

TXT records are public, and are often used by many tech services (e.g. Atlassian) for the purposes of client domain verification.

I thought it might be fun to see who is using what. 

Here's what I did:

1. Ran trawler.py on a list of domains in a CSV file. I took the top 1000 from [Cloudflare](https://radar.cloudflare.com/domains). 

2. A liittle bit of manual cleaning of TXT names

3. Uploaded to a Cloudflare KV

4. Created a lightweight website with simple.css and [DataTables](https://datatables.net)

5. Scripted a Cloudflare Worker (worker.js) to query and return the results

You can see my results here: [Enterprise Tech Stacks](https://enterprisetechstacks.pages.dev)