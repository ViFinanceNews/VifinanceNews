from ViFinanceCrawLib.QuantAna.QuantAna_albert import QuantAnaInsAlbert
# file_path = "/Users/davestrantien/Desktop/CS-3332/Code_Project/Project_Space/vifinancenews/multilingual_debiased-0b549669.ckpt"
# detox = Detoxify(model_type="original-small", checkpoint=file_path)

# text =  "I love F**** Hate U"
# res_1 = detox.predict(text)
# print(res_1)

import os

def find_ckpt_with_keyword(directory, keyword):
    """
    Recursively search for the first .ckpt file containing the keyword in its name.

    Args:
        directory (str): The root directory to start the search.
        keyword (str): The keyword to look for in the filename.

    Returns:
        str or None: The relative path to the matching .ckpt file, or None if not found.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ckpt") and keyword in file:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, start=directory)
                return relative_path
    return None

test = QuantAnaInsAlbert()
text =  "I love F**** Hate U"
res_1 = test.detect_toxicity(text)
print(res_1)
