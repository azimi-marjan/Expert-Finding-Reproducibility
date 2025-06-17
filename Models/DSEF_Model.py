import os
import math
from collections import defaultdict

class Author:
    def __init__(self, id):
        self.id = id
        self.articles = []
        self.PEQ_D = 0
        self.pe=0.0

    def add_article(self, article):
        self.articles.append(article)

class Article:
    def __init__(self, id):
        self.id = id
        self.authors = []
        self.pdqs = defaultdict(lambda: 0)
        self.ranks = defaultdict(lambda: 0)
        self.year = None
        self.citation_count=0

    def add_author(self, author):
        self.authors.append(author)

class Query:
    def __init__(self, id):
        self.id = id
        self.articles = []
        self.authors = []

    def sort_authors_peqd(self):
        #self.sorted_authors = sorted(self.authors, key=lambda x: x.PEQ_D, reverse=True)
        self.sorted_authors = sorted(self.authors, key=lambda x: (-x.PEQ_D, -int(x.id)))

class DocumentBasedMethod:
    def __init__(self):
        self.all_authors = {}
        self.articles = {}
        self.queries = []

    def read_queries_from_file(self, query_file):
        self.queries = []
        with open(query_file, 'r') as file:
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    query_number = parts[0].strip()
                    #print(query_number)
                    query_description = parts[1].strip()
                    self.queries.append(Query(query_number))
                    

    def read_all_articles1(self, file_path):
        print("read")
        with open(file_path, 'r') as file:
            lines = file.readlines()

        article = None
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line == "<DOCNO>":
                i += 1
                article_id = lines[i].strip()
                article = Article(article_id)
                print(article)
                self.articles[article_id] = article
            i += 1

    def set_authors(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) != 2:
                continue  # Skip invalid lines
            author_id, article_id = parts[0].strip(), parts[1].strip()

            # Ensure the article exists in the system
            if article_id not in self.articles:
                article = Article(article_id)
                self.articles[article_id] = article
            else:
                article = self.articles[article_id]

            # Ensure the author exists in the system
            if author_id not in self.all_authors:
                author = Author(author_id)
                self.all_authors[author_id] = author
            else:
                author = self.all_authors[author_id]

            # Establish relationships between authors and articles
            author.add_article(article)
            article.add_author(author)

    def set_citations(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            article_id, citation_count = line.strip().split('\t')
            if article_id in self.articles:
                self.articles[article_id].citation_count = int(citation_count)
    
    def set_degree(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        count=0
        for line in lines:
            a= line.strip().split('\t')
            author_id=a[0].strip()
            #print(author_id)
            indegree=float(a[1].strip())
            if author_id in self.all_authors:
                print("author_id")
                count+=1
                self.all_authors[author_id].pe = indegree    
        print(f"count is:{count}")              

    def read_all_articles(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        article = None
        i = 0
        while i < len(lines):
            line = lines[i].strip()
           
            if line == "<DOCNO>":
                
                i += 1
                article_id = lines[i].strip()
                article = Article(article_id)
                print(article)
                self.articles[article_id] = article
            elif line == "<YEAR>":
                i += 1
                year_str = lines[i].strip()
                try:
                    # Convert the year to float first and then cast to int to handle '2015.0'
                    year = int(float(year_str))
                    if article:
                        article.year = year
                except ValueError:
                    print(f"Invalid year format: {year_str}")
            i += 1
                

    def read_language_model(self, file_path):
        print("read language model")
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split()
            query_id = parts[0].strip()
            #article_id = parts[2].replace("doc", "")
            article_id = parts[2]
            if article_id not in self.articles:
                self.articles[article_id] = Article(article_id)
            article = self.articles[article_id]
            article.pdqs[query_id] = float(parts[4])
            article.ranks[query_id] = int(parts[3])
            for query in self.queries:
                if query.id == query_id:
                    query.articles.append(article)

    def set_authors_of_queries(self):
        for query in self.queries:
            for article in query.articles:
                for author in article.authors:
                    if author not in query.authors:
                        query.authors.append(author)

    def PEQ_article_based(self, query_file_path, output_file_path,phi=0.8 ):
    # Open the output file once
        with open(output_file_path, 'w') as output_file:
            with open(query_file_path, 'r') as file:
                lines = file.readlines()

        # Process each line in the query file
            for line in lines:
                query_id, terms = line.strip().split('\t')
                terms = terms.split()
                query = next(q for q in self.queries if q.id == query_id)

            # Calculate PEQ_D for each author in the query
                for author in query.authors:
                    for article in author.articles:
                        citation_count=article.citation_count
                        num_authors=len(article.authors)
                        p_e_d=1/num_authors if num_authors>0 else 0
                        #author_num = len(article.authors)
                        #PED = 1 / author_num
                        PDC = math.log(math.e+citation_count)
                        if article.year is not None:
                            current_year = 2012  # Assuming the current year is 2012
                            lambda_value = 0.1 # Decay rate, adjust as needed
                            PD = math.exp(-lambda_value * (current_year - article.year))
                            #citation_count=article.citation_count    
                        else:
                            PD = 1  # Default value if year is missing
                        PQD = article.pdqs[query_id]
                        rank = article.ranks[query_id]
                        rank_factor = (1 - phi) * (phi ** (rank - 1))
                        #print(author.pe)
                        author.PEQ_D += PQD*author.pe

            # Sort authors based on PEQ_D and take the top 10
                query.sort_authors_peqd()
                #sorted_authors = query.sorted_authors[:30]
                sorted_authors = query.sorted_authors 

            # Write results for the current query
                for rank, author in enumerate(sorted_authors, start=1):
                    # Format the output as: query_id, constant Q0, author_id with prefix doc, rank, PEQ_D score, Anserini
                    line = f"{query_id} Q0 {author.id} {rank} {author.PEQ_D:.6f} Anserini\n"
                    output_file.write(line)

                # Reset PEQ_D values after writing
                for author in query.authors:
                    author.PEQ_D = 0

        # Reset PEQ_D for all authors
        for author in self.all_authors.values():
            author.PEQ_D = 0


# Example Usage
method = DocumentBasedMethod()
method.read_queries_from_file("path/to/query.tsv")
method.read_all_articles("path/to/dataset.txt")
method.set_authors("path/to/author.txt")
method.set_citations("path/to/citation_count.txt")
method.set_degree("path/to/degree.txt")
method.read_language_model("path/to/language_model.txt")
method.set_authors_of_queries()
method.PEQ_article_based("path/to/query.tsv","path/to/result.txt")
