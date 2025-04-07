import os

# Define the directory paths
input_dir = "inputFiles/new"
output_dir = "outputFiles"

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

# Function to convert the input data into TTL format
def process_tree_line(line):
    parts = line.strip().split('\t')
    if len(parts) < 4:
        return None

    word_id, word, head_id, dep_type = parts[0], parts[1], parts[2], parts[3]

    if head_id == "0":
        # If head ID is 0, it's the root, generate only TreeWord definition
        treeword_rdf = f"""
### poas:poas/treeword_{word_id}
:treeword_{word_id} rdf:type owl:NamedIndividual ,
         :TreeWord ;
         :word "{word}"^^xsd:string ;
         rdfs:label "treeword_{word_id}" .
"""
        return None, treeword_rdf

    # Lookup full dependency type in the map without splitting
    dep_base, dep_sub = dependency_map.get(dep_type, (dep_type, "none"))

    # Generate the RDF blocks for non-root nodes
    dep_rdf = f"""
### poas:poas/dep_treeword_{word_id}
:dep_treeword_{word_id} rdf:type owl:NamedIndividual ;
         :isDependant_obj_0 :{dep_base}_{dep_sub} ;
         :isDependant_obj_1 :treeword_{head_id} ;
         rdfs:label "dep_treeword_{word_id}" .
"""

    word_rdf = f"""
### poas:poas/treeword_{word_id}
:treeword_{word_id} rdf:type owl:NamedIndividual ,
         :TreeWord ;
         :isChild :treeword_{head_id} ;
         :isDependant_subj :dep_treeword_{word_id} ;
         :word "{word}"^^xsd:string ;
         rdfs:label "treeword_{word_id}" .
"""

    return dep_rdf, word_rdf


# Function to generate RDF for a single file
def generate_ttl_file(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    ttl_content = """@prefix : <poas:poas/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2001/01/rdf-schema#> .

"""

    treewords_rdf = []
    depwords_rdf = []
    treeword_ids = []  # To collect all treeword IDs for the T object

    # Process each line in the input file
    for line in lines:
        result = process_tree_line(line)
        if result:
            dep_rdf, word_rdf = result
            if dep_rdf:
                depwords_rdf.append(dep_rdf)
            treewords_rdf.append(word_rdf)
            treeword_ids.append(f"treeword_{line.split()[0]}")

    # Concatenate all the RDF content
    ttl_content += "".join(depwords_rdf) + "\n" + "".join(treewords_rdf)

    with open(output_file, 'w') as outfile:
        outfile.write(ttl_content)


# Main function to process all files
def process_all_files():
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all input files and generate output TTL files
    for i, filename in enumerate(sorted(os.listdir(input_dir))):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_dir, filename)
            output_file = os.path.join(output_dir, f"output{i + 1:02d}.ttl")
            generate_ttl_file(input_file, output_file)
            print(f"Processed {input_file} -> {output_file}")

# Run the process
process_all_files()