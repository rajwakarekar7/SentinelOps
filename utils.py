def has_enough_parts(parts , required_lenght):

    return len(parts) >= required_lenght

def get_word(parts):

    return parts[1].lower()

def get_text(parts):

    return " ".join(parts[1:]).lower()