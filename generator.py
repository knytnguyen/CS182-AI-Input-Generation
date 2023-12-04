import torch
import os
import xml.etree.ElementTree as ET
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import random
import re

def split_text(text, max_chunks):
    sentences = re.split(r'(?<=[.!?]) +', text)
    random.shuffle(sentences)
    return sentences[:max_chunks]

def create_random_structure(generated_text):
    element_names = ['item', 'section', 'part', 'element', 'node']
    lines = split_text(generated_text, random.randint(2, 5))
    root = ET.Element(random.choice(element_names))

    for line in lines:
        sub_element = ET.SubElement(root, random.choice(element_names))
        sub_element.text = line.strip()

    return root

def generate_xml(prompt, model, tokenizer, device):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    output = model.generate(input_ids, max_length=200, do_sample=True)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

def main():
    model_name_or_path = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    output_dir = "generated_xmls"
    os.makedirs(output_dir, exist_ok=True)

    prompts = [
    "Here is an example XML file. Please generate another one. <doc> <clean> </clean> <dirty> A B </dirty> <mixed> A <clean> </clean> B <dirty> A B </dirty> C </mixed> </doc> ",
    "I need to create an XML schema to define the structure of an XML document and map out the relationship between elements.",
    "Please use this template to generate the xml file. template: <document><content> <par>Sentence 1</par> <par>Sentence 2</par> <par>Sentence 3</par> <par>Sentence 4</par> <par>Sentence 5</par> <par>Sentence 6</par> </content></document>",
    "Designing an XML file for a school schedule involves creating a structure that can encapsulate various elements like classes, times, instructors, and rooms",
    "Construct an XML file for a book with an author, book title, and publishing year of your choice."
    ]

    for i in range(5):
        generated_text = generate_xml(prompts[i], model, tokenizer, device)
        xml_root = create_random_structure(generated_text)

        file_name = f"generated_file_{i + 1}.xml"
        file_path = os.path.join(output_dir, file_name)
        ET.ElementTree(xml_root).write(file_path)

if __name__ == "__main__":
    main()