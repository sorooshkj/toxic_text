import pandas as pd

# Step 1: Function to load toxic words from a .txt file (one word per line)
def load_toxic_words_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        toxic_words = [line.strip().lower() for line in file if line.strip()]
    return toxic_words

# Step 2: Function to check if a post contains toxic words and return them
def get_toxic_words_in_post(post, toxic_words):
    post = post.lower()  # Convert post to lowercase for case-insensitive matching
    found_words = [word for word in toxic_words if word in post]  # Collect toxic words found in the post
    return found_words

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
        # Get toxic words in the post
        found_toxic_words = get_toxic_words_in_post(post, toxic_words)

        # Binary flag for toxicity: 1 if any toxic words are found, else 0
        toxic_score = 1 if found_toxic_words else 0

        # Join the found toxic words as a comma-separated string
        toxic_words_str = ', '.join(found_toxic_words)

        print(f"Post: {post[:30]}... | Toxic Score: {toxic_score} | Toxic Words: {toxic_words_str}")
        
        results.append({
            'post': post,
            'toxic_score': toxic_score,  # Binary flag for toxicity
            'toxic_word_count': len(found_toxic_words),  # Number of toxic words found
            'toxic_words_found': toxic_words_str  # Comma-separated list of toxic words found
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
