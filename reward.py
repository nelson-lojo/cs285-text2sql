from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3 as sq3


def get_spider_db(name: str):
    return f"spider/database/{name}/{name}.sqlite"

class SQLExecutionError(Exception):
    pass

def run_query_on_db(query: str, db: str):
    with sq3.connect(db) as conn:
        try:
            rows = conn.execute(query).fetchall()
        except (sq3.OperationalError, sq3.IntegrityError) as e:
            raise SQLExecutionError(f"Error when executing {query}: {e}")
    return rows

def get_similarity(candidate, reference) -> float:
    """
    Calculate the similarity between two strings using cosine similarity.

    Returns a float between 0 and 1. A value of 1 is an identical match.
    """
    # Vectorize the text using TF-IDF, limiting the number of features
    vectorizer = TfidfVectorizer(max_features=1000)

    # Calculate cosine similarity between the vectors
    similarity = cosine_similarity(
        vectorizer.fit_transform([reference]), 
        vectorizer.transform([candidate])
    )[0][0]

    return similarity

def get_row_diff(candidate_rows, solution_rows) -> float:
    candidate_set = set(candidate_rows)
    solution_set = set(solution_rows)
    
    num_excess_rows = len(candidate_set - solution_set)
    excess_proportion = num_excess_rows / len(candidate_set)
    
    num_missing_rows = len(solution_set - candidate_set)
    missing_proportion = num_missing_rows / len(solution_set)
    return (1-excess_proportion + 1-missing_proportion) / 2

def get_reward(db_name: str, candidate_query: str, solution_query: str):
    db_path = get_spider_db(db_name)
    
    try:
        rows = run_query_on_db(candidate_query, db_path)
    except SQLExecutionError as e:
        return get_similarity(candidate_query, solution_query)
    
    sol_rows = run_query_on_db(solution_query, db_path)
    
    return 1.0 + get_row_diff(rows, sol_rows)
