#!/usr/bin/env python3

import arxiv
import pandas as pd
from datetime import datetime, timedelta
import logging
from datetime import timezone

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def collect_papers_for_date_range(start_date, end_date):
    """
    Collect papers for a specific date range.
    
    Args:
        start_date: datetime object for range start (inclusive)
        end_date: datetime object for range end (inclusive)
    
    Returns:
        list: Papers in the date range
    """
    # Format dates for arXiv query
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    # Set up the arXiv search client
    client = arxiv.Client()
    
    # Create the search query for ML papers within date range
    search = arxiv.Search(
        query=f"cat:cs.LG AND submittedDate:[{start_str} TO {end_str}]",
        max_results=None,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    try:
        for result in client.results(search):
            paper_info = {
                'title': result.title,
                'authors': ', '.join(author.name for author in result.authors),
                'abstract': result.summary,
                'published_date': result.published.strftime('%Y-%m-%d'),
                'arxiv_id': result.entry_id.split('/')[-1],
                'url': result.entry_id
            }
            papers.append(paper_info)
            
            # Log progress
            if len(papers) % 100 == 0:
                logging.info(f"Collected {len(papers)} papers for date range {start_str} to {end_str}")
                
    except arxiv.UnexpectedEmptyPageError:
        logging.warning(f"Reached API limit for date range {start_str} to {end_str} after collecting {len(papers)} papers")
    except Exception as e:
        logging.error(f"Error collecting papers for date range {start_str} to {end_str}: {str(e)}")
        if not papers:
            raise
            
    return papers

def collect_recent_papers(days_back=180, chunk_size=15):
    """
    Collect papers from arXiv's Machine Learning section (cs.LG) from the past specified days.
    Uses date chunking to bypass API limits.
    
    Args:
        days_back (int): Number of days to look back (default: 180)
        chunk_size (int): Number of days per chunk (default: 15)
    
    Returns:
        list: List of dictionaries containing paper information
    """
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days_back)
    
    logging.info(f"Collecting papers from the last {days_back} days (since {start_date.strftime('%Y-%m-%d')})...")
    
    all_papers = []
    current_start = start_date
    
    while current_start < end_date:
        # Calculate chunk end date
        chunk_end = min(current_start + timedelta(days=chunk_size), end_date)
        
        # Collect papers for this chunk
        logging.info(f"Collecting papers from {current_start.strftime('%Y-%m-%d')} to {chunk_end.strftime('%Y-%m-%d')}...")
        chunk_papers = collect_papers_for_date_range(current_start, chunk_end)
        all_papers.extend(chunk_papers)
        
        # Move to next chunk
        current_start = chunk_end
        
        # Sleep between chunks to be nice to the API
        if current_start < end_date:
            logging.info("Sleeping between chunks...")
            import time
            time.sleep(3)
    
    logging.info(f"Successfully collected {len(all_papers)} papers from cs.LG in the specified timeframe")
    return all_papers

def save_papers(papers, output_file='recent_ml_papers.csv'):
    """
    Save the collected papers to a CSV file.
    
    Args:
        papers (list): List of paper dictionaries
        output_file (str): Path to save the CSV file
    """
    try:
        df = pd.DataFrame(papers)
        # Remove duplicates if any (can happen with overlapping date ranges)
        df = df.drop_duplicates(subset=['arxiv_id'])
        df.to_csv(output_file, index=False)
        logging.info(f"Successfully saved {len(df)} papers to {output_file}")
    except Exception as e:
        logging.error(f"Error saving papers to CSV: {str(e)}")
        raise

def main():
    try:
        # Collect papers
        papers = collect_recent_papers()
        
        # Save to CSV
        if papers:
            save_papers(papers)
        else:
            logging.error("No papers were collected")
        
    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        raise

if __name__ == "__main__":
    main() 