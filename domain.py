import os

# Full map for dependency type lookup
dependency_map = {
    "root": ("ROOT", "NONE"),
    "nsubj": ("NSUBJ", "NONE"),
    "obj": ("OBJ", "NONE"),
    "iobj": ("IOBJ", "NONE"),
    "nummod": ("NUMMOD", "NONE"),
    "ccomp": ("CCOMP", "NONE"),
    "xcomp": ("XCOMP", "NONE"),
    "acl": ("ACL", "NONE"),
    "advmod": ("ADVMOD", "NONE"),
    "advmod:mnr": ("ADVMOD", "MANNER"),
    "advmod:dgr": ("ADVMOD", "DEGREE"),
    "advmod:plc": ("ADVMOD", "PLACE"),
    "advmod:time": ("ADVMOD", "TIME"),
    "advmod:idf": ("ADVMOD", "INDEFINITE_FREQUENCY"),
    "advmod:df": ("ADVMOD", "DEFINITE_FREQUENCY"),
    "amod": ("AMOD", "NONE"),
    "amod:opn": ("AMOD", "OPINION"),
    "amod:size": ("AMOD", "SIZE"),
    "amod:pq": ("AMOD", "PHYSICAL_QUALITY"),
    "amod:shp": ("AMOD", "SHAPE"),
    "amod:age": ("AMOD", "AGE"),
    "amod:clr": ("AMOD", "COLOUR"),
    "amod:orgn": ("AMOD", "ORIGIN"),
    "amod:mtrl": ("AMOD", "MATERIAL"),
    "amod:type": ("AMOD", "TYPES"),
    "amod:prps": ("AMOD", "PURPOSE"),
    "aux": ("AUX", "NONE"),
    "cop": ("COP", "NONE"),
    "mark": ("MARK", "NONE"),
    "det": ("DET", "NONE"),
    "det:predet": ("DET", "PREDET"),
    "cc": ("CC", "NONE"),
    "compound": ("COMPOUND", "NONE"),
}


def clean_pattern(pattern):
    """
    Removes unnecessary characters from the input pattern like {, }, , and trims spaces.
    """
    return pattern.replace('{', '').replace('}', '').replace(',', '').strip()


def generate_rdf_block(relation1, subtype1, relation2, subtype2, position, reverse=False):
    """
    Generates an RDFF block for the given relations and subtypes. If reverse is True,
    the relations and subtypes are swapped, and the position is reversed.
    """
    # Adjust parameters based on the reverse flag
    if reverse:
        relation1, subtype1, relation2, subtype2 = relation2, subtype2, relation1, subtype1
        left_word = "FIRST_CHILD" if position == "after" else "SECOND_CHILD"
    else:
        left_word = "FIRST_CHILD" if position == "before" else "SECOND_CHILD"

    # Define rule and pair names
    rule_name = f"rule_{relation1}_{subtype1}_{relation2}_{subtype2}"
    pair_name = f"pair_{relation1}_{subtype1}_{relation2}_{subtype2}"

    # Create RDF block
    rdf_block = f"""
### poas:poas/{rule_name}
:{rule_name} rdf:type owl:NamedIndividual ,
             :RuleResult ;
             :firstChild :{relation1}_{subtype1} ;
             :secondChild :{relation2}_{subtype2} ;
             :leftWord :{left_word} ;
             rdfs:label "{rule_name}" .
"""
    return rdf_block


def process_line(line, output_file):
    """
    Processes each line, extracts the pattern, and writes the corresponding RDF blocks
    (both normal and reversed) to the output file.
    """
    # Split the pattern based on whitespace
    parts = clean_pattern(line).split()

    # Extract relations, subtypes, and position
    relation1, subtype1 = parts[0], parts[1]
    relation2, subtype2 = parts[2], parts[3]
    position = parts[4]

    # Convert to RDF (both original and reversed)
    rdf_block = generate_rdf_block(relation1, subtype1, relation2, subtype2, position)
    reverse_rdf_block = generate_rdf_block(relation1, subtype1, relation2, subtype2, position, reverse=True)

    # Write both versions to the output file
    output_file.write(rdf_block)
    output_file.write(reverse_rdf_block)


def process_file(input_file, output_file_path):
    """
    Reads the input file, processes each line, and writes the corresponding RDF blocks to the output file.
    """
    with open(input_file, 'r') as file, open(output_file_path, 'w') as output_file:
        for line in file:
            # Skip empty lines
            if line.strip():
                process_line(line, output_file)


def merge_files(file1_path, file2_path, output_file_path):
    """
    Merges the content of two files into a new output file.

    Parameters:
    - file1_path: Path to the first input file.
    - file2_path: Path to the second input file, which will be added after the first one.
    - output_file_path: Path to the output file where the merged content will be written.
    """
    try:
        # Open the first file in read mode and the second file in read mode
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            # Read content from both files
            file1_content = file1.read()
            file2_content = file2.read()

        # Open the output file in write mode
        with open(output_file_path, 'w') as output_file:
            # Write content from both files to the output file
            output_file.write(file1_content)
            output_file.write("\n")  # Optional: Add a newline between the contents
            output_file.write(file2_content)

        print(f"Files merged successfully into {output_file_path}")

    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# File paths for input and output
input_file = 'D:/Uni/Trees/Programs/Generator/domainGenerator/patterns.txt'
output_file_path = 'D:/Uni/Trees/Programs/Generator/domainGenerator/rdf_output.txt'

# Process the file and write RDF blocks to the output file
process_file(input_file, output_file_path)

print(f"RDF blocks written to {output_file_path}")

# Example usage
file1 = 'dependencies.txt'
file2 = 'rdf_output.txt'
output_file = 'domain.ttl'

merge_files(file1, file2, output_file)

output_file = 'D:/Uni/Trees/Exported/domain1.ttl'
merge_files(file1, file2, output_file)