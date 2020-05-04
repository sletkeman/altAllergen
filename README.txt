DESCRIPTION
 - Allergen Pre-processing
    - The allergen pre-processing consists of flagging each recipe in the database with the matching allergen categories and allergen ingredients based on the recipe's ingredients and instruction text. This stage takes a significant amount of time. It is not advised to re-run this step on the dataset for demo purposes.
 
 - Similarity Pre-processing
    - The similarity pre-processing involves first using NLP to pull out the food items from
      a recipes's ingredients, and then standardize them by cross referencing against a known
      food dictionary.
    - The preprocessed ingredients and recipes are then turned into a matrix that is MxN where
      M is the number of recipes, and N is the number of ingredients. The matrix is then used 
      to compare a given recipe's most similar alternative recipe by using a shared nearest neighbor
      algorithm to return the top X number of similar recipes

 - API
    - A Python Flask application that serves data to the UI

 - User Interface
    - A VueJs application


INSTALLATION
 - Allergen Pre-processing
   1. To install the requirements for the allergen processor, navigate to the processor directory
   2. Install the necessary requirements using the pip command: `pip install -r requirements.txt`
 
 - API
   1. pip install -r web_app/api/requirments.txt
   2. npm run --prefix web_app/web build

 - User Interface
   1. npm --prefix web_app/web i
   2. npm install -g @vue/cli


EXECUTION
 - Allergen Pre-processing
   1. To run the allergen processor and flag allergens in recipes, navigate to the processor directory
   2. Execute the python script from the command line `python allergen-processor.py`
   3. This will update the recipe collection with all potentially associated allergens

- Similarity Pre-processing
   1. The similarity pre-processing has already been done, and has dumped it's results to a
      JSON file. Running these python scripts takes appropimately 10 hours and should not be 
      run by the graders.

 - API
   1. sh ./web_app/setpath.sh python web_app/api/main.py

 - User Interface
   1. npm --prefix web_app/web serve

 DEMO
 - Access the live AWS instance at: http://ec2co-ecsel-1w78movq5gw2-1222388112.us-east-1.elb.amazonaws.com
 - View a sample demonstration at: 

 - User Interface
    - Access the live AWS instance at: http://ec2co-ecsel-1w78movq5gw2-1222388112.us-east-1.elb.amazonaws.com
    - The demo_screenshots folder contains sample usage and interesting search combinations to try out.
