
import difflib

converstion_context = {
    "last_subject": None
}

intent_patterns= {


    "/ask": [

        "tell me about",
        "what is",
        "who is",
        "information about",
        "explain"
    ],

    "/search": [

        "search for",
        "find",
        "look for"
    ],

    "/category": [

        "display",
        "show",
        "list"
    ]

}


def is_similar(user_text ,pattern):

    similarity = difflib.SequenceMatcher(
        None,
        user_text,
        pattern
    ).ratio()

    return similarity > 0.7


def process_natural_language(sentence):

    sentence = sentence.lower().strip()

    if "it" in sentence:

        last_subject = converstion_context["last_subject"]

        if last_subject:

            sentence =sentence.replace("it", last_subject)

    for command in intent_patterns:

        patterns = intent_patterns[command]

        for pattern in patterns:

            words = sentence.split()

            first_parts = " ".join(words[:len(pattern.split())])


            if pattern in sentence or is_similar(first_parts, pattern):


                pattern_length = len(pattern.split())

                extracted_words = words[pattern_length:]

                extracted = " ".join(extracted_words).strip()

                converstion_context["last_subject"]= extracted


                if extracted == "":

                    print("\n[NLP ERROR]")
                    print("No target detcted")

                    return None
                

                if command == "/category":

                    extracted = extracted.replace("memories", "").strip()

                
                generated_command = command + " " + extracted

                print("\n[NLP DEBUG]")
                print("INTENT:", command)
                print("EXTRACTED:", extracted)
                print("GENERATED_COMMAND:", generated_command)


                return generated_command
            
    return None



        

