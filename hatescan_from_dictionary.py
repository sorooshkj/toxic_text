import pandas as pd

# Step 1: Function to load toxic words from a .txt file (one word per line)
def load_toxic_words_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        toxic_words = [line.strip().lower() for line in file if line.strip()]
    return toxic_words

# Step 2: Function to check if a post contains toxic words
def count_toxic_words(post, toxic_words):
    post = post.lower()  # Convert post to lowercase for case-insensitive matching
    toxic_count = 0
    for word in toxic_words:
        if word in post:
            toxic_count += 1
    return toxic_count

# Process posts and check for toxic words
def process_posts(input_file, output_file, toxic_words_file):
    # Load toxic words from badwords.txt
    toxic_words = load_toxic_words_from_txt(toxic_words_file)

    # Read the Excel file containing posts
    df = pd.read_excel(input_file)

    # Select the first column (posts) regardless of its name
    posts = df.iloc[:, 0].tolist()

    results = []

    for post in posts:
        # Check for toxic words in the post
        toxic_count = count_toxic_words(post, toxic_words)

        # Binary flag for toxicity: 1 if any toxic words are found, else 0
        toxic_score = 1 if toxic_count > 0 else 0

        print(f"Toxic Score: {toxic_score} | Toxic Word Count: {toxic_count}")
        
        results.append({
            'post': post,
            'toxic_score': toxic_score,  # Binary flag for toxicity
            'toxic_word_count': toxic_count  # Number of toxic words found
        })

    # Convert the results list into a DataFrame
    result_df = pd.DataFrame(results)

    # Save the results to a new Excel file
    result_df.to_excel(output_file, index=False)

if __name__ == '__main__':
    input_file = 'blackpill-5000.xlsx'  # file with posts
    output_file = 'files/dictionary_processed_blackpill-5000.xlsx'  # Where to save the results
    toxic_words_file = 'files/badwords.txt'  # Your file with toxic words

    # Process the posts and save the results
    process_posts(input_file, output_file, toxic_words_file)
    print(f"Results saved to {output_file}")
