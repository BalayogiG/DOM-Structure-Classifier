# Packages for web scraping and visualization
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  
import warnings
warnings.filterwarnings('ignore')

# To clean HTML => removing all the unwanted tags from the web page source code
def cleanMe(html):
    soup = bs(html, "html5lib")
    [x.extract() for x in soup.find_all('script')]
    [x.extract() for x in soup.find_all('style')]
    [x.extract() for x in soup.find_all('meta')]
    [x.extract() for x in soup.find_all('noscript')]
    [x.extract() for x in soup.find_all('link')]
    [x.extract() for x in soup.find_all('br')]
    [x.extract() for x in soup.find_all(text=lambda text:isinstance(text, Comment))]
    return soup

# To analyse the DOM strcuture of the web page
def DOM_analysis(URL):

    # Reading the categories of the tags from the csv
    tags_categories = pd.read_csv('tags_categories.csv')

    # getting the source code of the web page using requests package.
    source_code = requests.get(URL)
    soup = bs(source_code.content, 'html.parser')
    soup = source_code.content

    # cleaning the html code
    cleaned_html = cleanMe(soup)
    tags_source = []
    tags_names = []

    # creating a list for the tag_names and tag_source block
    for x in cleaned_html.find_all(True):
        tags_source.append(x)
        tags_names.append(x.name)

    # creatingn DataFrame from the list
    tags_names_df = pd.DataFrame(tags_names, columns=['tags_names'], dtype='str')
    tags_source_df = pd.DataFrame(tags_source, columns=['tags_source'], dtype='str')

    # combining two DataFrames.
    combined_df = pd.concat([tags_names_df, tags_source_df], axis=1)

    # droping the top 2 rows => html and head tags
    m_df = combined_df[2:]
    m_df = m_df.reset_index(drop=True)

    # extracting the column values from the tags_categories DataFrame
    categories_col = tags_categories.columns.values
    tag_lst = m_df['tags_names']
    total_tags_cat = []

    # creating dictionary for the tag category and its count.
    data = dict()
    for i in categories_col:
        d = np.intersect1d(np.array(tags_categories[i].values, dtype=str), np.array(tag_lst.values, dtype=str))
        data[i] = {'tags': list(d), 'count': sum([list(tag_lst).count(j) for j in d])}

    # creating a list that contains all the values of counts from different tag categories
    for tag in categories_col:
        total_tags_cat.append(data[tag]['count'])

    return total_tags_cat, categories_col

def calculate_percentage(total_tags_cat):
    # finding the total summation of the values
    total_tags = sum(total_tags_cat)

    # calculation of percentage
    text_freq = total_tags_cat[0] * 100 / total_tags
    form_freq = total_tags_cat[1] * 100 / total_tags
    image_freq = total_tags_cat[2] * 100 / total_tags
    multimedia_freq = total_tags_cat[3] * 100 / total_tags
    links_freq = total_tags_cat[4] * 100 / total_tags
    table_freq = total_tags_cat[5] * 100 / total_tags

    # printing all the percentage of all the categories
    print("Text : {0:.2f}".format(text_freq)+"%")
    print("Form : {0:.2f}".format(form_freq)+"%")
    print("Image : {0:.2f}".format(image_freq)+"%")
    print("Multimedia : {0:.2f}".format(multimedia_freq)+"%")
    print("Links : {0:.2f}".format(links_freq)+"%")
    print("Table : {0:.2f}".format(table_freq)+"%")


def plot_DOM_Analysis(categories_col, total_tags_cat):
    # converting categories_col to list
    labels_values = categories_col.tolist()

    # ploting the bar chart
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(labels_values,total_tags_cat, color=['orange', 'red', 'green', 'blue', 'cyan', 'black'])
    #plt.tight_layout()
    colors = {'text':'orange', 'form':'red','image':'green','multimedia':'blue','links':'yellow','table':'black'}
    labels = list(colors.keys())
    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.title("DOM Structure Analysis ")
    plt.legend(handles,labels)
    plt.show()

def main():
    def main():
    URL = input("Enter url: ")
    t, c = DOM_analysis(URL)
    calculate_percentage(t)
    plot_DOM_Analysis(c ,t)

main()
