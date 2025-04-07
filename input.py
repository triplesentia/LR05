import os


# Function to generate RDF for a string of words
def generate_sentence_rdf(sentence):
    # Split the sentence string into a list of words
    word_list = sentence.strip().split()
    sentence_rdf = ""
    sentenceword_references = []  # List to store references to each sentence word

    # Loop through each word in the list and generate corresponding RDF
    for i, word in enumerate(word_list):
        word_id = i + 1  # Simple ID to track each word
        sentenceword_ref = f":sentenceword_{word_id}"
        sentenceword_references.append(sentenceword_ref)

        # Generate RDF for the word
        sentence_rdf += f"""
### poas:poas/sentenceword_{word_id}
{sentenceword_ref} rdf:type owl:NamedIndividual ,
         :SentenceWord ;
         :word "{word}"^^xsd:string ;
"""
        # Add :directlyToTheLeft if it's not the first word
        if i > 0:
            sentence_rdf += f'         :directlyToTheLeft :sentenceword_{i} ;\n'

        # Add label for the sentence word
        sentence_rdf += f'         rdfs:label "sentenceword_{word_id}" .\n'

    return sentence_rdf


# Function to append generated RDF to an existing RDF file
def append_to_existing_rdf(existing_rdf_path, sentence, output_rdf_path):
    # Generate the RDF content for the new sentence
    new_rdf_content = generate_sentence_rdf(sentence)

    # Read the existing RDF file content
    with open(existing_rdf_path, 'r') as existing_rdf_file:
        existing_rdf_content = existing_rdf_file.read()

    # Append the new RDF content
    combined_rdf_content = existing_rdf_content + "\n\n" + new_rdf_content

    # Write the combined content to the new output file
    with open(output_rdf_path, 'w') as output_rdf_file:
        output_rdf_file.write(combined_rdf_content)

    print(f"New RDF content successfully appended to {output_rdf_path}")


# Specify the path to the existing RDF file
existing_rdf = "outputFiles/output03.ttl"

# Specify the path where the updated RDF will be written
output_rdf = "generated/1.ttl"

# The sentence (input) to form RDF objects
sentence = "she always"

# Call the function to append the generated RDF to the existing file
append_to_existing_rdf(existing_rdf, sentence, output_rdf)

output_rdf = "D:/Uni/Trees/Exported/2.ttl"
append_to_existing_rdf(existing_rdf, sentence, output_rdf)

output_rdf = "D:/Uni/Trees/Exported/1.ttl"
append_to_existing_rdf(existing_rdf, sentence, output_rdf)