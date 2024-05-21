import re
from collections import Counter
from collections import OrderedDict
import math

def count_words_in_file(file_path):
    with open(file_path, 'r') as f:
        words = f.read().split()
        return sorted(Counter(words).items())

def main():
    test = []
    docnames = []
    preproc_docs = []

    with open('tfidf_docs.txt', 'r') as inputfile_list:
        for line in inputfile_list:
            doc_name = line.strip() #get rid of the new line and space each doc out individually.
            docnames.append(doc_name)

            with open(doc_name, 'r') as individual_file:
                doc_contents = individual_file.read()
            
            #now clean up the items inside the document as follows:
            
            #remove unnecessary symbols/special characters. Keep alphanumeric values and underscore:
            #remove website links:
            edited_docs = re.sub(r'https?://[^\s]+|www\.[^\s]+', '', doc_contents)
            edited_docs = re.sub(r'[^A-Za-z0-9_\s]+', '', edited_docs)
            edited_docs = re.sub(r'\s+', ' ', edited_docs)
            
            
            #remove trailing whitespaces:
            edited_docs = edited_docs.strip()
            
            #convert to words to lowercase.
            edited_docs = edited_docs.lower()
            
            #split the words in the text documents respectively:
            indiv_words = edited_docs.split()
            
            #remove stop words, mainly words in the file stopwords.txt:
            stopwords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
            
            remove_stopwords = [indiv_word for indiv_word in indiv_words if indiv_word not in stopwords]
            edited_docs = ' '.join(remove_stopwords)
            edited_docs = edited_docs.strip()

            indiv_words_v2 = edited_docs.split()
            
            
            indiv_words_v2 = [i.replace('ing', '') if i.endswith('ing') else i.replace('ly', '') if i.endswith('ly') else i.replace('ment', '') 
                          if i.endswith('ment') else i for i in indiv_words_v2]
            
            
            edited_docs = ' '.join(indiv_words_v2)
            edited_docs = edited_docs.strip()
        
        #append it on to a list to make things easier when copying onto a document.
            test.append(edited_docs)
        
    #Now create the new file copies (will accomodate for possible different file names now):
        
    for content, d in zip(test, docnames):
        finaldoc = f'preproc_{d}'
        preproc_docs.append(finaldoc)
        
        with open(finaldoc, 'w') as f: 
            f.write(content)

    #Store the preprocessed documents into a new document for easier traversal into the next part:
    preproc= open('preprocessed_docs.txt', 'w')
    for i in preproc_docs:
        preproc.write(i + '\n')
    preproc.close()


            
###############################################################################################


#if made into a function, it should take in a doc_name list.
#A: Compute word frequencies for each preprocessed document.

    counterlist = []
    total_words_in_documents = []

#per file copies do the traversal:
    with open('preprocessed_docs.txt', 'r') as f:
        for line in f:
            doc_name = line.strip()
            with open(doc_name, 'r') as f: 
                s = count_words_in_file(doc_name)
                counterlist.append(s)
                total_words_in_documents.append(len(f.read().split()))
        

    tf_calc = []

#Compute the term frequency for each Counter: TF(t) = (Number of times term t appears in a document) / (Total number of terms in the document)
    print(counterlist)

    traverse_total_words = iter(total_words_in_documents) 

    for i in counterlist:
        tf_per_doc = []
        total = next(traverse_total_words)
        for value in i:
            tf = value[1] / total
            print(value[1], total)
            tf_per_doc.append((value[0],tf))

        tf_calc.append(tf_per_doc)

#Compute the IDF for the shared words in the documents.

    doc_frequency = Counter()

    for sublist in counterlist:
        keys = [word for word, count in sublist]
        doc_frequency.update(keys)
    

    doc_frequency = sorted(doc_frequency.items())
    ordered_doc_freq = OrderedDict(doc_frequency)

    idf_calc = []

    for word in ordered_doc_freq:
    
        idf = math.log(len(counterlist) / ordered_doc_freq[word]) + 1
        idf_calc.append((word, idf))

#print(idf_calc)

#multiply the tf * idf now. Both of the lists are in consistent order and in tuple form corresponding to the word. This is the only way to match up everything accordingly

#to do this we traverse both lists out, append to a list in tuple format, each doc is rep by nested list.
    tf_idf_calc = []

    for doc_values in tf_calc:
        tf_idf_doc = []
        for i in doc_values:
            for word_value in idf_calc:
                if i[0] == word_value[0]:
                    tf_idf = round((i[1] * word_value[1]),2)
                    tf_idf_doc.append((i[0], tf_idf))
        tf_idf_calc.append(tf_idf_doc)
  

#Now sort the tfidf calculations in descending order. The higher tfidf score will be prioritized. 

    tf_idf_calc = [sorted(sublist, key=lambda x: (-x[1], x[0])) for sublist in tf_idf_calc]
#print(tf_idf_calc)

#after sorting and limiting, make the new file output files per respective document:

#for i in tf_idf_calc:
    #if len(i) > 5:   
        

#fix this so it doesn't need docnames list anymore.
    for index, (doc, i) in enumerate(zip(docnames, tf_idf_calc)):
        final = f'tfidf_{doc}'
        with open(final, 'w') as f:
            f.write(str(i[:5]) + '\n')



if __name__ == "__main__":
    main()