# Program to detect multiple alternatives in a class
import re


def parse(text, components):
    print('RE: TEXT', text)
    # Convert all component names to lower case
    for i in range(len(components)):
        components[i] = components[i].lower()

    # Stores the final output in string format
    output = ""

    # Converting text to lower case
    text = text.lower()

    # Components - Specify the list of components on flight
    # components = ['engine','gearbox','wing','brake']
    print("Components: ", components)

    # Regex to split the sentence into one or more sentences, questions etc
    split_pat = r".*?[\.\?\,]"
    sentences = re.findall(split_pat, text)
    print('Sentences: ', sentences)

    print(sentences)

    # Generating a string representing the or form of all the components available
    component_alt = "("
    for component in components:
        component_alt = component_alt + component + "|"
    component_alt = component_alt[0:len(component_alt) - 1] + ")"
    print("Component Alternatives:", component_alt)

    # Generating the regex pattern and regex object for component wise matching
    match_pat = component_alt
    match_rex = re.compile(match_pat, flags=re.IGNORECASE)

    # Pronount pat
    pronoun_alt = ".*(It|they|them).*"
    pronoun_pat = pronoun_alt
    pronoun_rex = re.compile(pronoun_pat, flags=re.IGNORECASE)

    # Initialize component descripition dictionary to store the description of each component
    component_desc = {}
    for component in components:
        component_desc[component] = []

    # Last appended list will store the list of components to which descritions were appended to for the
    # previous sentence
    last_appended = []

    # Split and append
    index = 0
    for sentence in sentences:
        components_matched = match_rex.findall(sentence)
        if len(components_matched) != 0:
            for component in components_matched:
                component_desc[component].append({'index': index, 'sentence': sentence})
        elif len(last_appended) != 0 and pronoun_rex.match(sentence):
            for component in last_appended:
                last_desc_idx = len(component_desc[component]) - 1
                new_desc = component_desc[component][last_desc_idx]['sentence'] + sentence
                component_desc[component][last_desc_idx]['sentence'] = new_desc
        last_appended = components_matched
        index +=1

    # print('Component descripitions: ', component_desc)
    # print("\n-----------------------------")
    # print('System Report (By Components)')
    # for component in components:
    #    print('Component:',component)
    #    if component_desc[component] == []:
    #        print('->  No description available')
    #    else:
    #        for desc in component_desc[component]:
    #            print('->', desc)
    # print("-----------------------------")

    """
    output += "-----------------------------"
    output += '\nSystem Report (By Components)'
    for component in components:
        output += '\n\nComponent: ' + component
        if not component_desc[component]:
            output += '\n->  No description available'
        else:
            for desc in component_desc[component]:
                output += '\n-> ' + desc
    output += "\n-----------------------------"
    """

    return component_desc
