### reads in the HTML files read by the crawler existing at the provided directory
### then generates the inverted index as tf-idf scores
### writes the inverted index to a .pkl file with name defined with output_pickle_file

from bs4 import BeautifulSoup
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict

html_dir_file_path = 'ir_crawler/directory_iit.edu' ## hard code directory of html files
def build_inverted_index(dir):
    print("Begin Building Inverted Index")
    print(f"Reading in .html files from Directory: {dir}")
    documents = [] ## list of docs which will be the HTML parsed text
    file_paths = [] ## relative file paths on machine which will be the document IDs

    ### reading in files from dir
    for file_name in os.listdir(dir):
        if file_name.endswith('.html'): ## read all .html
            file_path = os.path.join(dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')

                all_text = soup.get_text(separator=' ')

                # clean the text from the webpage -> removes \n chars
                cleaned_text = ' '.join(line.strip() for line in all_text.splitlines() if line.strip())
                documents.append(cleaned_text) ## list of doc text
                file_paths.append(file_path) ## list of file paths

                ### so now we have a 1-1 list of documents their related file paths (docIDs)

    print("Done reading... Vectorizing documents")
    # lower case the words and remove stop words (maybe keep them)
    # ### - REMEMBER: now must lowercase query in preprocessing
    vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
    tfidf_matrix = vectorizer.fit_transform(documents) ### passing list of documents to vectorizor to create tf-idf
    print("Tfidf scores done calculating")

    print("Building inverted index")
    # Build inverted index
    inverted_index = defaultdict(dict)

    terms = vectorizer.get_feature_names_out() ## gets list of all terms
    for term_index, term in enumerate(terms):
        for doc_index in range(len(documents)):
            tfidf_score = tfidf_matrix[doc_index, term_index]
            if tfidf_score > 0: ## if score is zero - toss it
                ### create tf-idf score for given term and doc pair or append to list already there
                inverted_index[term][file_paths[doc_index]] = tfidf_score
    print("Done building inverted index")

    return dict(inverted_index)

def save_inverted_index(inverted_index, output_file):
    print("Saving as .pkl file")
    with open(output_file, 'wb') as f:
        pickle.dump(inverted_index, f)

    print(f".pkl file saved to {output_file}")

if __name__ == '__main__':
    ### input own directory if re-scraped not iit.edu but will default to iit.edu
    ## change domain to the domain that was scraped by the spider in the ir_crawler

    ## defines the expected html directory name and the output index file name
    #### based on the domain defined above which should be same as defined in the crawler allowed_domains attribute

    html_directory = html_dir_file_path
    output_pickle_file = f'iit.edu_inverted_index.pkl' ## change if the html directory changes

    inverted_index = build_inverted_index(html_directory)
    save_inverted_index(inverted_index, output_pickle_file)
