# datascience_assignment1

Goal: Uses a selection of the Google Books Ngram dataset to detect a Volcano erruption in a given year throughout history.
This approach is Boolean; True/False whether there was a Volcano Erruption (not consdering multiple events or small activity).
Accomplished by training with a preassembled list of Volcanic events from ~1500-2008 (the range of the data set)
  Google Books Ngrams: http://storage.googleapis.com/books/ngrams/books/datasetsv2.html
  
Keywords used to train:
  volcano, eruption,lava,igneous,volcanic activity, volcanic erruption, molten
Keywords deemed less helpful:
  magma,

Overview of Code Approach:

Order of tasks:
  DATA GATHERING (Once, in order to save time): 
    Import and words and their count (remove extraneous words from files, volume_count, and page_count)
    Import total_counts (words per year)
    Divide by word_count by total_count
    Normalize the data (remains to be seen if truly necessary)
    Store the data locally

  DATA PROCESSING:
    Import cleaned word_data (word, normalized count)
    Import training volcano_data (Year's of Vocanic events)
    
    Link word_data to volcano_data
    Possibly perform some processing
      Shift all years by some (TBD) integer amount (motivation: better match volcanic erruptions to peaks of words use)
      Consider the neighbouring years somehow
    
    Separate train and test data
      Two possible approaches to separation:
        Cut (train data from before a given year and test data after a given year)
        Sample (train and test randomly sampled from throughout full data set)
      Secondary consideration percentage of spliting between test/train (60/40, 70/30, 80/20... etc.)
      
      
